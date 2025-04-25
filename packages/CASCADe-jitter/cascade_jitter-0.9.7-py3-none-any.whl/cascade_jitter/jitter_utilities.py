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

import math
import numpy as np
from scipy import ndimage
from skimage.transform import warp
from skimage._shared.utils import safe_as_int
from skimage.transform import rotate

__all__ = ['derotate_data_cube', 'pad_region_of_interest_to_square', 'pad_to_size',
           'warp_polar', 'highpass']

def derotate_data_cube(data_cube : np.ndarray, angles : np.ndarray,
                       ROI : np.ndarray = None, order : int = 3,
                       is_padded : bool = True) -> np.ndarray:
    """
    Derotate spectral image cube.

    Parameters
    ----------
    data_cube : 'np.ndarray' of 'float'
        Input image to be de-rotated by 'angle' degrees.
    ROI : 'np.ndarray' of 'bool'
        Region of interest (default None)
    angles : 'np.ndarray' of 'float'
        Rotaton angles in degrees for each integration in the data cube.
    order : 'int'
        Order of the used interpolation in the rotation function of the
        skimage package.
    is_padded : 'bool'
        Indicated if input data is already zero padded

    Returns
    -------
    derotated_data_cube : '2-D ndarray' of 'float'
        The zero padded and derotated image.
    """
    if not is_padded:
        d, h, w = data_cube.shape
        required_image_size = int(np.sqrt(h**2 + w**2))

        if ROI is None:
            ROI = np.zeros((h, w), dtype=bool)

        padded_cube = pad_region_of_interest_to_square(data_cube, ROI)
        padded_cube = \
            pad_to_size(padded_cube, required_image_size, required_image_size)
    else:
        padded_cube = data_cube

    derotated_data_cube = np.zeros_like(padded_cube)
    for i, image in enumerate(padded_cube):
        derotated_image = rotate(image, angles[i], order=order)
        derotated_data_cube[i, ...] = derotated_image

    return derotated_data_cube


def pad_region_of_interest_to_square(data_cube : np.ndarray, ROI : np.ndarray,
                                     mask_data_cube : np.ndarray = None) -> np.ndarray:
    """
    Pad ROI to square.

    Zero pad the extracted Region Of Interest of a larger image such that the
    resulting images in the data cube are square.

    Parameters
    ----------
    data_cube : 'np.ndarray' of 'float'
        Input data cube to be zero padded.
    ROI : 'np.ndarray' of 'bool'
        Region of interest for all data.
    mask_data_cube : 'np.ndarray' of 'bool' (optional)
        Boolean mask belonging to input data_cube, default is None

    Returns
    -------
    padded_data_cube : 'np.ndarray' of 'float'
        Padded data_cube.
    """
    if mask_data_cube is not None:
        label_im, _ = ndimage.label(
            ~(np.tile(ROI, (data_cube.shape[0], 1, 1)) | mask_data_cube))
    else:
        label_im, _ = ndimage.label(~np.tile(ROI, (data_cube.shape[0], 1, 1)))
    slice_z, slice_y, slice_x = ndimage.find_objects((label_im == 1).astype(int))[0]

    padded_data_cube = data_cube[slice_z, slice_y, slice_x].copy()

    if mask_data_cube is not None:
        padded_data_cube[mask_data_cube[slice_z, slice_y, slice_x]] = 0.0

    d, h, w = padded_data_cube.shape
    if h == w:
        return padded_data_cube

    im_size = np.max([h, w])
    delta_h = im_size - h
    delta_w = im_size - w
    padding = ((0, 0),
               (delta_h//2, delta_h-(delta_h//2)),
               (delta_w//2, delta_w-(delta_w//2)))
    padded_data_cube = np.pad(padded_data_cube,
                          padding, 'constant', constant_values=(0.0))

    return padded_data_cube


def pad_to_size(data_cube : np.ndarray, h : int, w : int,
                mask_data_cube : np.ndarray = None) -> np.ndarray:
    """
    Zero pad the input image to an image of hight h and width w.

    Parameters
    ----------
    data_cube : 'np.ndarray' of 'float'
        Input spectral data cube to be zero-padded to a cube of images of size (h, w).
    h : 'int'
        Hight (number of rows) of output images.
    w : 'int'
        Width (number of columns) of output images.
    mask_data_cube : 'np.ndarray' of 'bool', (optional)
        Data cube mask. default value is None

    Returns
    -------
    padded_cube : 'np.ndarray' of 'float'
        Padded data cube
    """
    padded_cube = data_cube.copy()
    if mask_data_cube is not None:
        padded_cube[mask_data_cube] = 0.0
    d_image, h_image, w_image = padded_cube.shape
    npad_h = np.max([1, (h-h_image)//2])
    npad_w = np.max([1, (w-w_image)//2])
    padding = ((0, 0), (npad_h, npad_h), (npad_w, npad_w))
    padded_cube = np.pad(padded_cube,
                          padding, 'constant', constant_values=(0.0))
    return padded_cube


def _log_polar_mapping(output_coords, k_angle, k_radius, center):
    """
    Inverse mapping function to convert from cartesion to polar coordinates.

    Parameters
    ----------
    output_coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the output image
    k_angle : float
        Scaling factor that relates the intended number of rows in the output
        image to angle: ``k_angle = nrows / (2 * np.pi)``
    k_radius : float
        Scaling factor that relates the radius of the circle bounding the
        area to be transformed to the intended number of columns in the output
        image: ``k_radius = width / np.log(radius)``
    center : tuple (row, col)
        Coordinates that represent the center of the circle that bounds the
        area to be transformed in an input image.

    Returns
    -------
    coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the input image that
        correspond to the `output_coords` given as input.
    """
    angle = output_coords[:, 1] / k_angle
    rr = ((np.exp(output_coords[:, 0] / k_radius)) * np.sin(angle)) + center[0]
    cc = ((np.exp(output_coords[:, 0] / k_radius)) * np.cos(angle)) + center[1]
    coords = np.column_stack((cc, rr))
    return coords


def _linear_polar_mapping(output_coords, k_angle, k_radius, center):
    """
    Inverse mapping function to convert from cartesion to polar coordinates.

    Parameters
    ----------
    output_coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the output image
    k_angle : float
        Scaling factor that relates the intended number of rows in the output
        image to angle: ``k_angle = nrows / (2 * np.pi)``
    k_radius : float
        Scaling factor that relates the radius of the circle bounding the
        area to be transformed to the intended number of columns in the output
        image: ``k_radius = ncols / radius``
    center : tuple (row, col)
        Coordinates that represent the center of the circle that bounds the
        area to be transformed in an input image.

    Returns
    -------
    coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the input image that
        correspond to the `output_coords` given as input.
    """
    angle = output_coords[:, 1] / k_angle
    rr = ((output_coords[:, 0] / k_radius) * np.sin(angle)) + center[0]
    cc = ((output_coords[:, 0] / k_radius) * np.cos(angle)) + center[1]
    coords = np.column_stack((cc, rr))
    return coords


def warp_polar(image, center=None, *, radius=None, rotation_angle_oversampling=1,
               output_shape=None, scaling='linear', multichannel=False,
               **kwargs):
    """
    Remap image to polor or log-polar coordinates space.

    Parameters
    ----------
    image : ndarray
        Input image. Only 2-D arrays are accepted by default. If
        `multichannel=True`, 3-D arrays are accepted and the last axis is
        interpreted as multiple channels.
    center : tuple (row, col), optional
        Point in image that represents the center of the transformation (i.e.,
        the origin in cartesian space). Values can be of type `float`.
        If no value is given, the center is assumed to be the center point
        of the image.
    radius : float, optional
        Radius of the circle that bounds the area to be transformed.
    AngleOversampling : int
        Oversample factor for number of angles
    output_shape : tuple (row, col), optional
    scaling : {'linear', 'log'}, optional
        Specify whether the image warp is polar or log-polar. Defaults to
        'linear'.
    multichannel : bool, optional
        Whether the image is a 3-D array in which the third axis is to be
        interpreted as multiple channels. If set to `False` (default), only 2-D
        arrays are accepted.
    **kwargs : keyword arguments
        Passed to `transform.warp`.

    Returns
    -------
    warped : ndarray
        The polar or log-polar warped image.

    Examples
    --------
    Perform a basic polar warp on a grayscale image:
    >>> from skimage import data
    >>> from skimage.transform import warp_polar
    >>> image = data.checkerboard()
    >>> warped = warp_polar(image)
    Perform a log-polar warp on a grayscale image:
    >>> warped = warp_polar(image, scaling='log')
    Perform a log-polar warp on a grayscale image while specifying center,
    radius, and output shape:
    >>> warped = warp_polar(image, (100,100), radius=100,
    ...                     output_shape=image.shape, scaling='log')
    Perform a log-polar warp on a color image:
    >>> image = data.astronaut()
    >>> warped = warp_polar(image, scaling='log', multichannel=True)
    """
    if image.ndim != 2 and not multichannel:
        raise ValueError("Input array must be 2 dimensions "
                         "when `multichannel=False`,"
                         " got {}".format(image.ndim))

    if image.ndim != 3 and multichannel:
        raise ValueError("Input array must be 3 dimensions "
                         "when `multichannel=True`,"
                         " got {}".format(image.ndim))

    if center is None:
        center = (np.array(image.shape)[:2] / 2) - 0.5

    if radius is None:
        w, h = np.array(image.shape)[:2] / 2
        radius = np.sqrt(w ** 2 + h ** 2)

    if output_shape is None:
        height = 360*rotation_angle_oversampling
        width = int(np.ceil(radius))
        output_shape = (height, width)
    else:
        output_shape = safe_as_int(output_shape)
        height = output_shape[0]
        width = output_shape[1]

    if scaling == 'linear':
        k_radius = width / radius
        map_func = _linear_polar_mapping
    elif scaling == 'log':
        k_radius = width / np.log(radius)
        map_func = _log_polar_mapping
    else:
        raise ValueError("Scaling value must be in {'linear', 'log'}")

    k_angle = height / (2 * np.pi)
    warp_args = {'k_angle': k_angle, 'k_radius': k_radius, 'center': center}

    warped = warp(image, map_func, map_args=warp_args,
                  output_shape=output_shape, **kwargs)

    return warped


def highpass(shape : int) -> np.ndarray:
    """
    Return highpass filter to be multiplied with fourier transform.

    Parameters
    ----------
    shape : 'ndarray' of 'int'
        Input shape of 2d filter

    Returns
    -------
    filter
        high pass filter
    """
    x = np.outer(
        np.cos(np.linspace(-math.pi/2., math.pi/2., shape[0])),
        np.cos(np.linspace(-math.pi/2., math.pi/2., shape[1])))
    return (1.0 - x) * (2.0 - x)


def hanning_window(shape : int) -> np.ndarray:
    """
    Create 2d hanning window.

    Parameters
    ----------
    shape : 'int'
        Input window size.

    Returns
    -------
    han2d : 'np.ndarray' of 'float'
        2D hanning window.

    """
    h = np.hanning(shape)
    han2d = np.outer(h, h)  # 2D Hanning window
    return han2d