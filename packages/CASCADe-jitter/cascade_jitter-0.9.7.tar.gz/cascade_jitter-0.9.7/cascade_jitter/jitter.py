#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of the CASCADe package which has been
# developed within the ExoplANETS-A H2020 program.
#
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2022  Jeroen Bouwman
#import ast
import os
import numpy as np
import pathlib
import math
#import configparser
from typing import Tuple
from tqdm.auto import tqdm
from skimage.registration import phase_cross_correlation
#from skimage.transform import warp
#from skimage._shared.utils import safe_as_int
#from skimage.transform import rotate
#from skimage.transform import SimilarityTransform
#from sklearn.preprocessing import RobustScaler

from cascade_filtering.filtering import EdgeFilter
from cascade_filtering.kernel import create_gaussian_kernel
from cascade_filtering.filtering import prepare_data_for_filtering
from cascade_filtering.filtering import filter_image_cube

from cascade_jitter.utilities import check_configuration_files
from cascade_jitter.utilities import read_configuration_files
from cascade_jitter import least_squares
from cascade_jitter.jitter_utilities import derotate_data_cube
from cascade_jitter.jitter_utilities import pad_to_size
from cascade_jitter.jitter_utilities import pad_region_of_interest_to_square
from cascade_jitter.jitter_utilities import highpass
from cascade_jitter.jitter_utilities import hanning_window
from cascade_jitter.jitter_utilities import warp_polar
from cascade_jitter import __path__

__all__ = ['Tracer', 'JitterDetector']

CONFIG_PATH = pathlib.Path(os.path.dirname(__path__[0])) / 'configuration_files/'


class Tracer:
    """
    Tracer class.

    This class contains all functionality to determine the spectral trace of the
    dispersed light in spectral image cubes.
    """
    def __init__(self, configuration_file : str = 'tracer.conf',
                 configuration_file_path : pathlib.Path = CONFIG_PATH) -> None:
        self.configuration = self.get_configuration(configuration_file,
                                                    configuration_file_path)

    def get_configuration(self, configuration_file : str = 'tracer.conf',
                          configuration_file_path : pathlib.Path = CONFIG_PATH):
        """
        Get the configuration parameters.

        Parameters
        ----------
        configuration_file : str, optional
            DESCRIPTION. The default is 'tracer.conf'.
        configuration_file_path : pathlib.Path, optional
            DESCRIPTION. The default is CONFIG_PATH.

        Returns
        -------
        configuration : 'dict'
            Dictionary containing all configuration parameters

        """
        configuration_file = check_configuration_files(configuration_file,
                                                       configuration_file_path)
        configuration = read_configuration_files(configuration_file)
        configuration['configuration_file_path'] = configuration_file_path
        return configuration

    def run_tracer(self, data_cube : np.ndarray,
                   data_cube_mask : np.ndarray) -> None:
        """
        Run all trace determinations and polynomial fits to spectral data cube.

        Parameters
        ----------
        data_cube : 'np.ndarray' of 'float'
            Input spectral data cube.
        data_cube_mask : 'np.ndarray' of 'bool'
            Boolean mask of input data cube.

        Returns
        -------
        None

        """
        (trace_per_source, source_mask, roi, number_of_sources,
         edge_filter_configuration) = self.trace_from_edge_filter(
            data_cube, data_cube_mask,
            self.configuration['trace_filter_config_file'],
            self.configuration['configuration_file_path']
            )
        trace_per_source_col = self.center_of_light(
            data_cube, source_mask
            )
        trace_parameters = self.fit_trace(
            trace_per_source,
            self.configuration['trace_order'],
            edge_filter_configuration['extension_extraction_height']+2
            )
        trace_parameters_col = self.fit_trace(
            trace_per_source_col,
            self.configuration['trace_order'],
            edge_filter_configuration['extension_extraction_height']+2
            )
        self.spectral_traces = {'col': {'trace': trace_per_source_col,
                                        'trace_par': trace_parameters_col},
                                'sod': {'trace': trace_per_source,
                                        'trace_par': trace_parameters}
                                }
        self.source_mask = source_mask
        self.roi = roi
        self.number_of_sources = number_of_sources
        self.edge_filter_configuration = edge_filter_configuration

    def center_of_light(self, data_cube : np.ndarray,
                        data_cube_mask : np.ndarray) -> list:
        """
        Calculate the center of light position.

        Parameters
        ----------
        data_cube : 'np.ndarray' of 'float'
            Input data cube, with dimensions number of integrations, number of
            wavelengthpoints and number of cross dispersion pixels.
        data_cube_mask : 'np.ndarray' of 'bool'
            Boolean mask attached to data cube.

        Returns
        -------
        trace_per_source : 'list' of 'tuple'
            Center of light spectral trace for each source and integration.

        """
        if data_cube_mask.ndim == 3:
            trace_mask = data_cube_mask[None, ...]
        else:
            trace_mask = data_cube_mask
        nsources, nintegrations, nwavelength, nspatial = trace_mask.shape

        trace_per_source = []
        weights = np.tile(np.arange(nspatial), (nwavelength, 1))
        for mask in ~trace_mask:
            source_traces_per_integration = []
            for iint, sub_mask in enumerate(mask):
                extraction_mask = (sub_mask).astype(int)
                COL = np.sum(data_cube[iint, ...] *
                             weights*extraction_mask, axis=-1) / \
                        (np.sum(data_cube[iint, ...] *
                                extraction_mask, axis=-1)+1.e-14)
                mask = np.all(~sub_mask, axis=-1)
                source_traces_per_integration.append((COL[~mask],
                                                      np.arange(nwavelength)[~mask]))
            trace_per_source.append(source_traces_per_integration)

        return trace_per_source

    def trace_from_edge_filter(self, data_cube : np.ndarray,
                               data_cube_mask : np.ndarray,
                               configuration_file : str = 'edge_filter.conf',
                               path : pathlib.Path = CONFIG_PATH) -> \
                                                 Tuple[list, np.ndarray]:
        """
        Determine the spectral trace using the CASCADe-filtering package.

        Parameters
        ----------
        data_cube : 'np.ndarray'
            Input spectral data cube.
        data_cube_mask : 'np.ndarray'
            Boolean mask of data cube.
        configuration_file : 'str', optional
            Configuration file. The default is 'edge_filter.conf'.
        path : 'pathlib.Path', optional
            Path to the configuration file. The default is CONFIG_PATH.

        Returns
        -------
        trace_pere_source : 'list'
            Spectral trace points for each source and integration in data cube.
        trace_mask : 'np.ndarray'
            Location mask of sources for each integration in spactral data cube.

        """
        EF = EdgeFilter(configuration_file=configuration_file, path=path)
        EF.run_filter(data_cube, data_cube_mask)
        EF.derive_source_location()

        edge_filter_configuration = EF.configuration
        number_of_sources = EF.source_location.number_of_sources
        trace_per_source = EF.source_location.source_traces
        #trace_mask = EF.source_location.trace_mask
        source_mask = EF.source_location.source_mask
        roi = EF.source_location.roi

        return (trace_per_source, source_mask, roi, number_of_sources,
                edge_filter_configuration)

    def fit_trace(self, trace : list, order : int = 1, edge : int = 2) -> list:
        """
        Fit a polynomial to the trace points.

        Parameters
        ----------
        trace : 'np.ndarray'
            Input spectral trace points
        order : 'int', optional
            Polynomial order. The default is 1.
        edge: 'int', optinal
            number of pixels to be suppressed at the edges of the trace range.

        Returns
        -------
        list
            Fitted polynomial coefficients.

        """
        delta = least_squares.create_regularization_matrix('value', order+1, 1)
        alpha = least_squares.return_lambda_grid(1.e-6, 1.e6, 20)

        trim_range = np.arange(edge)

        trace_parameters = []
        for trace_per_source in trace:
            trace_parameters_per_int = []
            for trace_per_int in trace_per_source:
                Y = trace_per_int[1]
                X = trace_per_int[0]
                if len(Y) <= 2*edge:
                    par = np.array([np.nan]*(order+1))
                    trace_parameters_per_int.append(par)
                    continue
                W = np.array([Y**i for i in range(order+1)]).T
                cov_matrix = np.identity(Y.size)
                cov_matrix[trim_range, trim_range] = 1.e8
                cov_matrix[-trim_range-1, -trim_range-1] = 1.e8
                par, *_ = least_squares.ridge(W, X, cov_matrix, delta, alpha)
                trace_parameters_per_int.append(par)
        trace_parameters.append(trace_parameters_per_int)
        return trace_parameters


class JitterDetector:
    """
    JitterDetector class.

    This class contains all functionality to determine relative movement and
    distortion of the dispersed light in spectral image cubes.
    """
    def __init__(self, configuration_file : str = 'jitter_detector.conf',
                 configuration_file_path : pathlib.Path = CONFIG_PATH) -> None:
        self.configuration = self.get_configuration(configuration_file,
                                                    configuration_file_path)


    def get_configuration(self, configuration_file : str = 'jitter_detector.conf',
                          configuration_file_path : pathlib.Path = CONFIG_PATH):
        """
        Get the configuration parameters.

        Parameters
        ----------
        configuration_file : str, optional
            Name of the configuration file. The default is 'jitter_detector.conf'.
        configuration_file_path : pathlib.Path, optional
            Path to configuration file. The default is CONFIG_PATH.

        Returns
        -------
        configuration : 'dict'
            Dictionary containing all configuration parameters

        """
        configuration_file = check_configuration_files(configuration_file,
                                                       configuration_file_path)
        configuration = read_configuration_files(configuration_file)
        configuration['configuration_file_path'] = configuration_file_path
        return configuration


    def run_jitter_detection(self, data_cube : np.ndarray,
                             mask_data_cube : np.ndarray,
                             ROI : np.ndarray,
                             reference_data_cube : np.ndarray = None,
                             mask_reference_data_cube : np.ndarray = None) -> None:
        """
        Run jitter detection of data.

        Parameters
        ----------
        data_cube : 'np.ndarray' of 'float'
            Input data cube.
        mask_data_cube : 'np.ndarray' of bool
            Mask of input data cube.
        ROI : 'np.ndarray' of 'bool'
            Region of interest.
        reference_data_cube : 'np.ndarray' of 'float', optional
            Reference data cube, if None than spectral images of the input
            data cube are used. The default is None.
        mask_reference_data_cube : 'np.ndarray' of 'bool', optional
            Mask of reference data cube. The default is None.

        Returns
        -------
        None

        """
        if reference_data_cube is None:
            reference_data_cube = \
                data_cube[self.configuration['jitter_reference_integrations'], ...]
            mask_reference_data_cube = \
                mask_data_cube[self.configuration['jitter_reference_integrations'], ...]
        self.reference_data_cube = reference_data_cube
        self.mask_reference_data_cube = mask_reference_data_cube

        if self.configuration['jitter_determine_shift_only']:
            print("Preprocessing Data")
            pp_data_cube = pre_process_data(
                data_cube, mask_data_cube, ROI,
                sigma_kernel=self.configuration['jitter_preprocess_kernel_sigma'],
                kernel_size=self.configuration['jitter_preprocess_kernel_size']
            )
            pp_reference_data_cube = pre_process_data(
                reference_data_cube, mask_reference_data_cube, ROI,
                sigma_kernel=self.configuration['jitter_preprocess_kernel_sigma'],
                kernel_size=self.configuration['jitter_preprocess_kernel_size']
            )
            print("Determining Poining Movement")
            self.source_shifts = determine_relative_source_shift(
                pp_data_cube,
                pp_reference_data_cube,
                upsample_factor=self.configuration['jitter_upsample_factor']
             )
        else:
            print("Preprocessing Data")
            pp_data_cube, rotation_angle_oversampling = pre_process_data(
                data_cube, mask_data_cube, ROI,
                sigma_kernel=self.configuration['jitter_preprocess_kernel_sigma'],
                kernel_size=self.configuration['jitter_preprocess_kernel_size'],
                rotation_angle_oversampling=self.configuration['jitter_rotation_angle_oversampling']
            )
            pp_reference_data_cube, _ = pre_process_data(
                reference_data_cube, mask_reference_data_cube, ROI,
                sigma_kernel=self.configuration['jitter_preprocess_kernel_sigma'],
                kernel_size=self.configuration['jitter_preprocess_kernel_size'],
                rotation_angle_oversampling=self.configuration['jitter_rotation_angle_oversampling']
            )
            self.rotation_angle_oversampling = rotation_angle_oversampling
            self.upsample_factor = self.configuration['jitter_upsample_factor']

            fft_data_cube = fft_process_data(pp_data_cube)
            fft_reference_data_cube = fft_process_data(pp_reference_data_cube)
            print("Determining Rotation and Scale")
            self.distortions = determine_relative_rotation_and_scale(
                fft_data_cube,
                fft_reference_data_cube,
                upsample_factor=self.upsample_factor,
                rotation_angle_oversampling=self.rotation_angle_oversampling
            )
            print("Determining Poining Movement")
            source_shifts = np.zeros_like(self.distortions)
            for iref, distortion in enumerate(self.distortions):
                derotated_pp_data_cube = \
                    derotate_data_cube(pp_data_cube, -distortion[:, 0],
                                       order=3, is_padded=True)
                source_shifts[iref:iref+1, ...] = determine_relative_source_shift(
                    derotated_pp_data_cube,
                    pp_reference_data_cube[iref:iref+1, ...],
                    upsample_factor=self.upsample_factor
                )
                self.source_shifts = source_shifts

def pre_process_data(data_cube : np.ndarray, mask_data_cube : np.ndarray,
                     ROI : np.ndarray,
                     rotation_angle_oversampling : int = None,
                     sigma_kernel : float = 1.0,
                     kernel_size : int = 11) -> np.ndarray:
    """
    Preprocess data for image registration.

    Parameters
    ----------
    data_cube : 'np.ndarray' of 'float'
        Input data cube.
    mask_data_cube : 'np.ndarray' of 'bool'
        Mask belonging to input data cube..
    ROI : 'np.ndarray' of 'bool'
        Region of interest for all integrations
    rotation_angle_oversampling : int, optional
        required oversampling factor for rotation determination.
        The default is None.

    Returns
    -------
    pre_processed_data_cube : 'np.ndarray'
        Pre processed data cube.

    """
    # Gaussian convolution with sigma of 1 pxel to ensure image registration
    # for undersampled data
    kernel = create_gaussian_kernel(kernel_size, sigma_kernel)
    kernel = kernel[None, ...]
    (pp_image_cube, pp_mask_cube, _, pp_roi_image_cube_index ,
     pp_data_cube_valid_index, filtered_data_valid_index) = \
        prepare_data_for_filtering(data_cube, mask_data_cube,
                                   kernel_stack_shape=kernel.shape,
                                   ROI=ROI
                                   )
    filtered_image_cube = \
        filter_image_cube(pp_image_cube, pp_mask_cube,  kernel)
    filtered_image_cube = \
        filtered_image_cube[filtered_data_valid_index][0, ...]
    filtered_image_cube_mask = ~pp_mask_cube[pp_data_cube_valid_index].astype(bool)

    ROI_filtered = np.zeros(filtered_image_cube.shape[1:], dtype=bool)
    pre_processed_data_cube = \
        pad_region_of_interest_to_square(filtered_image_cube, ROI_filtered,
                                         filtered_image_cube_mask)

    if rotation_angle_oversampling is not None:
        # image size for angle determination, 1 larger than angle oversampling
        # in polar images.
        used_angle_oversampling = int(rotation_angle_oversampling) + 1
        number_of_angles = 360
        required_image_size = 2*used_angle_oversampling*number_of_angles

        # minimum image size for derotation
        h, w = data_cube.shape[1:]
        minimum_image_size = int(np.sqrt(h**2 + w**2))
        # scaling requred image size and effective angle oversampling
        scaling = minimum_image_size/required_image_size
        if scaling > 1.0:
            used_angle_oversampling = math.ceil(used_angle_oversampling*scaling)

        pre_processed_data_cube = pad_to_size(pre_processed_data_cube,
                                              required_image_size,
                                              required_image_size)

        return pre_processed_data_cube, used_angle_oversampling-1

    return pre_processed_data_cube


def determine_relative_source_shift(target_data_cube : np.ndarray,
                                    reference_data_cube : np.ndarray,
                                    upsample_factor : int = 111,
                                    space : str ='real') -> np.ndarray:
    """
    Determine the relative shift of the spectral images.

    This routine determine the relative shift between a reference spectral
    image and another spectral image.

    Parameters
    ----------
    reference_image : 'np.ndarray' of 'float'
        Reference spectral image
    target_data_cube : 'np.ndarray' of 'float'
        Spectral image
    upsample_factor : 'int', optional
        Default value is 111
    space : 'str', optional
        Default value is 'real'

    Returns
    -------
    relative_image_shifts : 'np.ndarray' of 'float'
        Relative spectral image shitfts compared to the reference_cube
        The relative shifts are difined as follows:
        relative_image_shifts[ #refs, #targets, 0]
           relative shift compared to the reference image in the dispersion
           direction of the light (from top to bottom, shortest wavelength should
           be at row 0. Note that this shift is defined such that shifting a
           spectral image by this amound will place the trace at the exact same
           position as that of the reference image
        relative_image_shifts[ #refs, #targets, 1]
           relative shift compared to the reference image in the cross-dispersion
           direction of the light (from top to bottom, shortest wavelength should
           be at row 0. Note that this shift is defined such that shifting a
           spectral image by this amound will place the trace at the exact same
           position as that of the reference image.

    Raises
    ------
    ValueError
        If shape of reference images are not the same as the target images.

    Notes
    -----
        The input data cubes need to be pre-processed i.e. convolved and
        zero padded.
    """
    if reference_data_cube.shape[1:] != target_data_cube.shape[1:]:
        raise ValueError("Images should have the same size.")

    relative_image_shifts = np.empty((reference_data_cube.shape[0],
                                      target_data_cube.shape[0], 2))

    for ir, ref_image in enumerate(tqdm(reference_data_cube, leave='True',
                                   desc="Reference Image", colour='blue',
                                   position=0, total=reference_data_cube.shape[0])):
        for it, target_image in enumerate(tqdm(target_data_cube, leave=False,
                                          desc="Target Image", colour='red',
                                          position=1, total=target_data_cube.shape[0])):
            shift, _, _ = \
                phase_cross_correlation(ref_image, target_image,
                                        upsample_factor=upsample_factor,
                                        space=space, normalization=None)
            relative_image_shifts[ir, it, :] = -shift

    return relative_image_shifts


def fft_process_data(data_cube: np.ndarray) -> np.ndarray:
    """
    Create a cube of FFT magnitude images.

    Parameters
    ----------
    data_cube : 'np.ndarray' of 'float'
        Input data cube

    Returns
    -------
    fft_data_cube : 'np.ndarray' of 'float'
        Outout data cube of FFT magnitudes.

    Notes
    -----
    The input data cube is expected to be pre-processed i.e. gaussian convolved
    and zero-padded.

    """
    if data_cube.ndim == 3:
        han = np.tile(hanning_window(data_cube.shape[1]),
                      (data_cube.shape[0], 1, 1))
        fft_data_cube = np.abs(
            np.fft.fftshift(np.fft.fftn(data_cube*han, axes=(1,2)), axes=(1,2))
        )**2
    else:
        han = hanning_window(data_cube.shape[0])
        fft_data_cube = np.abs(np.fft.fftshift(np.fft.fftn(data_cube*han)))**2

    return fft_data_cube


def determine_relative_rotation_and_scale(target_data_cube : np.ndarray,
                                           reference_data_cube : np.ndarray,
                                           upsample_factor : int = 111,
                                           rotation_angle_oversampling : int = 2) -> np.ndarray:
    """
    Determine the relative rotation and scalng changes.

    This routine determines the relative rotation and scale change between
    an reference spectral image and another spectral image.

    Parameters
    ----------
    target_data_cube : 'np.ndarray' of 'float'
        Input data cube of pre-processed, FFT-ed spectral images
    reference_data_cube : 'np.ndarray' of 'float'
       Reference data cube of  pre-processed, FFT-ed spectral images.
    upsample_factor : 'int', optional
        Upsampling factor of FFT image used to determine sub-pixel shift.
        By default set to 111.
    rotation_angle_oversampling : 'int', optional
        Upsampling factor of the FFT image in polar coordinates for the
        determination of sub-degree rotation. Set by default to 2.

    Returns
    -------
    relative_image_distortion : 'np.ndarray' of 'float'
        relative_image_distortion[#ref, #target, 0] are the
        relative rotation angle in degrees. The angle is defined such that the
        image needs to be rotated by this angle to have the same orientation
        as the reference spectral image.
        relative_image_distortion[#ref, #target, 1] are the
        relative spectral image scalings

    Raises
    ------
    ValueError
        If shape of reference images are not the same as the target images.

    Notes
    -----
    Input target and reference data cubes need to be preprocessed and FFT-ed

    """
    if reference_data_cube.shape[1:] != target_data_cube.shape[1:]:
        raise ValueError("Images should have the same size.")

    h, w = target_data_cube.shape[1:]
    radius = 0.8*np.min([w/2, h/2])

    hpf = highpass((h, w))

    relative_image_distortion = np.empty((reference_data_cube.shape[0],
                                      target_data_cube.shape[0], 2))
    for ir, ref_image in enumerate(tqdm(reference_data_cube, leave='True',
                                   desc="Reference Image", colour='blue',
                                   position=0, total=reference_data_cube.shape[0])):
        for it, target_image in enumerate(tqdm(target_data_cube, leave=False,
                                          desc="Target Image", colour='red',
                                          position=1, total=target_data_cube.shape[0])):

            ref_image_filtered = ref_image * hpf
            warped_fft_ref_im = \
                warp_polar(ref_image_filtered, scaling='log',
                           radius=radius, output_shape=None,
                           multichannel=None,
                           rotation_angle_oversampling=rotation_angle_oversampling)
            target_image_filtered = target_image * hpf
            warped_fft_im = \
                warp_polar(target_image_filtered, scaling='log',
                           radius=radius, output_shape=None,
                           multichannel=None,
                           rotation_angle_oversampling=rotation_angle_oversampling)

            tparams = phase_cross_correlation(warped_fft_ref_im, warped_fft_im,
                                              upsample_factor=upsample_factor,
                                              space='real')

            shifts = tparams[0]
            # calculate rotation
            # rotation angle in counter clockwise direction
            # note, only look for angles between +- 90 degrees,
            # remove any flip of 180 degrees due to search
            shiftr, shiftc = shifts[:2]
            shiftr = shiftr/rotation_angle_oversampling
            if shiftr > 90.0:
                shiftr = shiftr-180.0
            if shiftr < -90.0:
                shiftr = shiftr+180.0
            relative_rotation = shiftr

            # Calculate scale factor from translation
            klog = radius / np.log(radius)
            relative_scaling = 1 / (np.exp(shiftc / klog))

            relative_image_distortion[ir,it, 0] = relative_rotation
            relative_image_distortion[ir,it, 1] = relative_scaling

    return relative_image_distortion

