#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from cascade_jitter.jitter_utilities import derotate_data_cube
from cascade_jitter.jitter_utilities import pad_region_of_interest_to_square
from cascade_jitter.jitter_utilities import pad_to_size
#  cascade_jitter.jitter_utilities import warp_polar
from cascade_jitter.jitter_utilities import highpass
from cascade_jitter.jitter_utilities import hanning_window

class TestJitterUtils(unittest.TestCase):
    def setUp(self):
        self.test_number_of_integrations = 50
        self.test_image_size = (21,21)
        self.test_padded_image_size = (51, 31)
        self.test_image_radius = int(np.sqrt(self.test_image_size[0]**2 +
                                        self.test_image_size[1]**2))

        test_image_cube = np.zeros((self.test_number_of_integrations,) +
                                   self.test_image_size)
        test_image_cube[:, :, 10] = 1.0
        self.test_image_cube = test_image_cube

        test_image_cube_mask = np.zeros_like(test_image_cube, dtype=bool)
        self.empty_test_image_cube_mask = test_image_cube_mask

        test_image_cube_mask2 = np.zeros_like(test_image_cube, dtype=bool)
        test_image_cube_mask2[:, 4, 3] = True
        test_image_cube_mask2[:, 0, 10] = True
        self.test_image_cube_mask = test_image_cube_mask2

        ROI = np.ones(self.test_image_size, dtype=bool)
        ROI[:, 8:13] = False
        self.ROI = ROI

        ROI = np.zeros(self.test_image_size, dtype=bool)
        self.empty_ROI = ROI

        self.test_angles = np.full((self.test_number_of_integrations), -90.0)

    def tearDown(self):
        del self.test_image_size
        del self.test_number_of_integrations
        del self.test_padded_image_size
        del self.test_image_radius
        del self.test_image_cube
        del self.ROI
        del self.empty_ROI
        del self.test_angles
        del self.test_image_cube_mask
        del self.empty_test_image_cube_mask


    def test_pad_to_size(self):
        h, w = self.test_padded_image_size
        y_start = (h - self.test_image_size[0])//2
        padded_image_cube = pad_to_size(self.test_image_cube, h, w)
        assert(padded_image_cube.shape[1:] == (h,w))
        assert(np.allclose(padded_image_cube[:, 0:y_start, :], 0.0))

    def test_pad_roi_to_square(self):
        padded_image = \
            pad_region_of_interest_to_square(self.test_image_cube, self.ROI)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               self.test_image_size[0])
        assert(np.allclose(padded_image[:, :, 10], 1))

        padded_image = \
           pad_region_of_interest_to_square(self.test_image_cube, self.empty_ROI)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               self.test_image_size[0])
        assert(np.allclose(padded_image[:, :, 10], 1))

        padded_image = \
            pad_region_of_interest_to_square(self.test_image_cube, self.ROI,
                                             mask_data_cube=self.test_image_cube_mask)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               (self.test_image_size[0]-1))
        assert(np.allclose(padded_image[:, 1:, 10], 1))
        assert(np.allclose(padded_image[:, 0, 10], 0))

        padded_image = \
           pad_region_of_interest_to_square(self.test_image_cube, self.ROI,
                                            mask_data_cube=self.empty_test_image_cube_mask)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               self.test_image_size[0])
        assert(np.allclose(padded_image[:, :, 10], 1))

        padded_image = \
            pad_region_of_interest_to_square(self.test_image_cube, self.empty_ROI,
                                             mask_data_cube=self.test_image_cube_mask)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               (self.test_image_size[0]-1))
        assert(np.allclose(padded_image[:, 1:, 10], 1))
        assert(np.allclose(padded_image[:, 0, 10], 0))

        padded_image = \
           pad_region_of_interest_to_square(self.test_image_cube, self.empty_ROI,
                                            mask_data_cube=self.empty_test_image_cube_mask)
        assert(padded_image.shape == (self.test_number_of_integrations,) +
               self.test_image_size)
        assert(int(np.sum(padded_image)) == self.test_number_of_integrations *
               self.test_image_size[0])
        assert(np.allclose(padded_image[:, :, 10], 1))


    def test_derotate(self):
        derotated_image_cube = derotate_data_cube(self.test_image_cube,
                                              self.test_angles, is_padded=False)
        assert(derotated_image_cube.shape[1:] == (self.test_image_radius,
                                                  self.test_image_radius))
        assert(np.allclose(self.test_image_cube[:, :, 10], 1.0))
        x_start = (self.test_image_radius - self.test_image_size[0])//2
        assert(np.allclose(derotated_image_cube[:, 10+x_start, x_start:-x_start],
                           1.0))

    def test_highpass(self):
        assert(np.allclose(highpass((1,1)), 2.0))
        assert(np.allclose(highpass((2,2)), 2.0))
        assert(np.allclose(highpass((3,3))[:, 0], 2.0))
        assert(np.allclose(highpass((3,3))[:, 2], 2.0))
        assert(np.allclose(highpass((3,3))[0, :], 2.0))
        assert(np.allclose(highpass((3,3))[2, :], 2.0))
        assert(highpass((3,3))[1,1] == 0.0)

    def test_hannimg(self):
        assert(hanning_window(3).shape == (3,3))

    def test_warp_polar(self):
        pass

if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJitterUtils)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)