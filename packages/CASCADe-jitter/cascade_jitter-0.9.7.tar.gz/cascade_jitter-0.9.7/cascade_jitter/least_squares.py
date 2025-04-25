#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:18:02 2022

@author: bouwman
"""
import numpy as np
#from types import SimpleNamespace
#import itertools
from collections.abc import Iterable
#import ast
#import warnings
#import time as time_module
#import copy
import ray
#from numba import jit
from scipy.linalg import svd
from scipy.linalg import solve_triangular
from scipy.linalg import cholesky
#import astropy.units as u
#from sklearn.decomposition import PCA
#from sklearn.preprocessing import StandardScaler

__all__ = ['ols', 'rayOLS', 'ridge', 'rayRidge', 'return_lambda_grid',
           'create_regularization_matrix']

def ols(design_matrix, data, covariance=None):
    r"""
    Ordinary least squares.

    Parameters
    ----------
    design_matrix : 'numpy.ndarray'
        The design or regression matrix used in the regression modeling
    data : 'numpy.ndarray'
        Vecor of data point to be modeled.
    weights : 'numpy.ndarray', optional
        Weights used in the regression. Typically the inverse of the
        coveraice matrix. The default is None.

    Returns
    -------
    fit_parameters : 'numpy.ndarray'
        Linear regirssion parameters.
    err_fit_parameters : 'numpy.ndarray'
        Error estimate on the regression parameters.
    sigma_hat_sqr : 'float'
        Mean squared error.

    Notes
    -----
    This routine solves the linear equation

    .. math:: A x = y

    by finding optimal solution :math:'\hat{x}' by minimizing

    .. math::

        || y - A*\hat{x} ||^2

    For details on the implementation see [1]_, [2]_, [3]_, [4]_

    References
    ----------
    .. [1] PHD thesis by Diana Maria SIMA, "Regularization techniques in
           Model Fitting and Parameter estimation", KU Leuven 2006
    .. [2] Hogg et al 2010, "Data analysis recipies: Fitting a model to data"
    .. [3] Rust & O'Leaary, "Residual periodograms for choosing regularization
           parameters for ill-posed porblems"
    .. [4] Krakauer et al "Using generalized cross-validationto select
           parameters in inversions for regional carbon fluxes"

    Examples
    --------
    >>> import numpy as np
    >>> from cascade.cpm_model import solve_linear_equation
    >>> A = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1], [1, 1, 0], [-1, 1, 0]])
    >>> coef = np.array([4, 2, 7])
    >>> b = np.dot(A, coef)
    >>> b = b + np.random.normal(0.0, 0.01, size=b.size)
    >>> results = solve_linear_equation(A, b)
    >>> print(results)
    """
    if not isinstance(covariance, type(None)):
        Gcovariance = cholesky(covariance, lower=True)
        weighted_design_matrix = solve_triangular(Gcovariance, design_matrix,
                                                  lower=True,
                                                  check_finite=False)
        data_weighted = solve_triangular(Gcovariance, data, lower=True,
                                         check_finite=False)
        scaling_matrix = np.diag(np.full(len(data_weighted),
                                 1.0/np.mean(data_weighted)))
        data_weighted = np.dot(scaling_matrix, data_weighted)
        weighted_design_matrix = np.dot(scaling_matrix, weighted_design_matrix)
    else:
        weighted_design_matrix = design_matrix
        data_weighted = data
    dim_dm = weighted_design_matrix.shape
    if dim_dm[0] - dim_dm[1] < 1:
        AssertionError("Wrong dimensions of design matrix: \
                                 more regressors as data; Aborting")

    # First make SVD of design matrix A
    U, sigma, VH = svd(weighted_design_matrix)

    # residual_not_reg = (u[:,rnk:].dot(u[:,rnk:].T)).dot(y)
    residual_not_reg = np.linalg.multi_dot([U[:, dim_dm[1]:],
                                            U[:, dim_dm[1]:].T, data_weighted])

    # calculate the filter factors
    F = np.identity(sigma.shape[0])
    Fsigma_inv = np.diag(1.0/sigma)

    # Solution of the linear system
    fit_parameters = np.linalg.multi_dot([VH.T, Fsigma_inv,
                                          U.T[:dim_dm[1], :], data_weighted])

    # calculate the general risidual vector (b-model), which can be caculated
    # by using U1 (mxn) and U2 (mxm-n), with U=[U1,U2]
    residual_reg = residual_not_reg + \
        np.linalg.multi_dot([U[:, :dim_dm[1]], np.identity(dim_dm[1]) - F,
                             U[:, :dim_dm[1]].T, data_weighted])

    effective_degrees_of_freedom = (dim_dm[0] - dim_dm[1])
    sigma_hat_sqr = np.dot(residual_reg.T, residual_reg) / \
        effective_degrees_of_freedom

    # calculate the errors on the fit parameters
    err_fit_parameters = np.sqrt(sigma_hat_sqr *
                                 np.diag(np.linalg.multi_dot([VH.T,
                                                              Fsigma_inv**2,
                                                              VH])))
    return fit_parameters, err_fit_parameters, sigma_hat_sqr


rayOLS = ray.remote(num_returns=3)(ols)


def ridge(input_regression_matrix, input_data, input_covariance,
          input_delta, input_alpha):
    r"""
    Ridge regression.

    Parameters
    ----------
    input_regression_matrix : 'numpy.ndarray'
        The design or regression matrix used in the regularized least square
        fit.
    input_data : 'numpy.ndarray'
        Vector of data to be fit.
    input_covariance : 'numpy.ndarray'
        Covariacne matrix used as weight in the least quare fit.
    input_delta : 'numpy.ndarray'
        Regularization matrix. For ridge regression this is the unity matrix.
    input_alpha : 'float' or 'numpy.ndarray'
        Regularization strength.

    Returns
    -------
    beta : 'numpy.ndarray'
        Fitted regression parameters.
    rss : 'float'
        Sum of squared residuals.
    mse : 'float'
        Mean square error
    degrees_of_freedom : 'float'
        The effective degress of Freedo of the fit.
    model_unscaled : 'numpy.ndarray'
        The fitted regression model.
    optimal_regularization : 'numpy.ndarray'
        The optimal regularization strength determened by generalized cross
        validation.
    aicc : float'
        Corrected Aikake information criterium.

    Notes
    -----
    This routine solves the linear equation

    .. math:: A x = y

    by finding optimal solution :math:'\^x' by minimizing

    .. math::
        || y - A*\hat{x} ||^2 + \lambda * || \hat{x} ||^2

    For details on the implementation see [5]_, [6]_, [7]_, [8]_

    References
    ----------
    .. [5] PHD thesis by Diana Maria SIMA, "Regularization techniques in
           Model Fitting and Parameter estimation", KU Leuven 2006
    .. [6] Hogg et al 2010, "Data analysis recipies: Fitting a model to data"
    .. [7] Rust & O'Leaary, "Residual periodograms for choosing regularization
           parameters for ill-posed porblems"
    .. [8] Krakauer et al "Using generalized cross-validationto select
           parameters in inversions for regional carbon fluxes"

    Examples
    --------
    >>> import numpy as np
    >>> from cascade.cpm_model import solve_linear_equation
    >>> A = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1], [1, 1, 0], [-1, 1, 0]])
    >>> coef = np.array([4, 2, 7])
    >>> b = np.dot(A, coef)
    >>> b = b + np.random.normal(0.0, 0.01, size=b.size)
    >>> results = solve_linear_equation(A, b)
    >>> print(results)

    """
    n_data, n_parameter = input_regression_matrix.shape

    # Get data and regression matrix
    Gcovariance = cholesky(input_covariance, lower=True)
    regression_matrix = solve_triangular(Gcovariance, input_regression_matrix,
                                         lower=True, check_finite=False)
    data = solve_triangular(Gcovariance, input_data, lower=True,
                            check_finite=False)
    scaling_matrix = np.diag(np.full(len(data),
                                     1.0/np.mean(data)))
    data = np.dot(scaling_matrix, data)
    regression_matrix = np.dot(scaling_matrix, regression_matrix)

    # Start of regression with SVD
    U, D, Vh = svd(regression_matrix, full_matrices=False, check_finite=False,
                   overwrite_a=True, lapack_driver='gesdd')
    R = np.dot(U, np.diag(D))
    delta = np.dot(np.dot(Vh, input_delta), Vh.T)
    RY = np.dot(R.T, data)
    unity_matrix_ndata = np.identity(n_data)

    if isinstance(input_alpha, Iterable):
        gcv_list = []
        mse_list = []
        for alpha_try in input_alpha:
            F = np.diag(D**2) + alpha_try*delta
            G = cholesky(F, lower=True)
            x = solve_triangular(G, R.T, lower=True, check_finite=False)
            H = np.dot(x.T, x)

            residual = np.dot(unity_matrix_ndata-H, data)
            rss = np.dot(residual.T, residual)
            degrees_of_freedom = np.trace(H)
            if (n_data-degrees_of_freedom) >= 1:
                mse = rss/(n_data-degrees_of_freedom)
                gcv = n_data*(np.trace(unity_matrix_ndata-H))**-2 * rss
            else:
                mse = 1.e16
                gcv = 1.e16
            gcv_list.append(gcv)
            mse_list.append(mse)
        opt_idx = np.argmin(gcv_list)
        optimal_regularization = input_alpha[opt_idx]
    else:
        optimal_regularization = input_alpha
    # Solve linear system with optimal regularization
    F = np.diag((D)**2) + optimal_regularization*delta
    G = cholesky(F, lower=True)
    x = solve_triangular(G, R.T, lower=True, check_finite=False)
    H = np.dot(x.T, x)

    x = solve_triangular(G, RY, lower=True, check_finite=False)
    x = solve_triangular(G.T, x, lower=False, check_finite=False)
    beta = np.dot(Vh.T, x)

    residual = np.dot(unity_matrix_ndata-H, data)
    rss = np.dot(residual.T, residual)
    degrees_of_freedom = np.trace(H)
    mse = rss/(n_data-degrees_of_freedom)
    aicc = n_data*np.log(rss) + 2*degrees_of_freedom + \
        (2*degrees_of_freedom * (degrees_of_freedom+1)) / \
        (n_data-degrees_of_freedom-1)

    # model_optimal = np.dot(H, data)
    model_unscaled = np.dot(input_regression_matrix, beta)

    return beta, rss, mse, degrees_of_freedom, model_unscaled, \
        optimal_regularization, aicc


rayRidge = ray.remote(num_returns=7)(ridge)


def return_lambda_grid(lambda_min, lambda_max, n_lambda):
    """
    Create grid for regularization parameters lambda.

    Parameters
    ----------
    lambda_min : TYPE
        DESCRIPTION.
    lambda_max : TYPE
        DESCRIPTION.
    n_lambda : TYPE
        DESCRIPTION.

    Returns
    -------
    lambda_grid : TYPE
        DESCRIPTION.

    """
    delta_lam = np.abs(np.log10(lambda_max)-np.log10(lambda_min))/(n_lambda-1)
    lambda_grid = 10**(np.log10(lambda_min) +
                       np.linspace(0, n_lambda-1, n_lambda)*delta_lam)
    return lambda_grid

def create_regularization_matrix(method, n_regressors, n_not_regularized):
    """
    Create regularization matrix.

    Two options are implemented: The first one 'value' returns a penalty
    matrix for the clasical ridge rigression. The second option 'derivative'
    is consistend with fused ridge penalty (as introduced by Goeman, 2008).

    Parameters
    ----------
    method : 'string'
        Method used to calculated regularization matrix. Allawed values
        are 'value' or 'derivative'
    n_regressors : 'int'
        Number of regressors.
    n_not_regularized : 'int'
        Number of regressors whi should not have a regulariation term.

    Raises
    ------
    ValueError
        Incase the method input parameter has a wrong value a ValueError is
        raised.

    Returns
    -------
    delta : 'ndarray'
        Regularization matrix.

    """
    allowed_methods = ['value', 'derivative']
    if method not in allowed_methods:
        raise ValueError("regularization method not recognized. "
                         "Allowd values are: {}".format(allowed_methods))
    if method == 'value':
        # regularization on value
        delta = np.diag(np.zeros((n_regressors)))
        delta[n_not_regularized:, n_not_regularized:] += \
            np.diag(np.ones(n_regressors-n_not_regularized))
    elif method == 'derivative':
        # regularazation on derivative
        delta_temp = np.diag(-np.ones(n_regressors-n_not_regularized-1), 1) +\
            np.diag(-1*np.ones(n_regressors-n_not_regularized-1), -1) + \
            np.diag(2*np.ones(n_regressors-n_not_regularized))
        delta_temp[0, 0] = 1.0
        delta_temp[-1, -1] = 1.0
        delta = np.diag(np.zeros((n_regressors)))
        delta[n_not_regularized:, n_not_regularized:] += delta_temp
    return delta