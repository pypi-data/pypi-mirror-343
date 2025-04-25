#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import os
import numpy as np
from cascade_jitter import jitter


class TestJitter(unittest.TestCase):
    def setUp(self):
        self.nref=3
        self.nintegrations = 50
        self.nwavelengths = 400
        self.nspatial = 70
        self.test_data_cube = np.zeros((self.nintegrations, self.nwavelengths,
                                        self.nspatial))
        self.test_data_cube[:, 100:300, 35] = 255.0
        self.test_data_cube_mask = np.ones_like(self.test_data_cube, dtype=bool)
        self.test_data_cube_mask[:, 100:300, 24:46] = False
        self.fit_order = 2

        ROI = np.ones((self.nwavelengths, self.nspatial), dtype=bool)
        ROI[90:310, 24:46] = False
        self.ROI = ROI

        self.reference_data_cube = np.zeros((self.nref, self.nwavelengths,
                                              self.nspatial))
        self.reference_data_cube[:, 101:301, 34] = 255.0
        self.reference_data_cube_mask = np.zeros_like(self.reference_data_cube,
                                                     dtype=bool)
        self.empty_test_data_cube_mask = np.zeros((self.nintegrations, self.nwavelengths,
                                                   self.nspatial), dtype=bool)

    def tearDown(self):
        del self.test_data_cube
        del self.test_data_cube_mask
        del self.nintegrations
        del self.nwavelengths
        del self.nspatial
        del self.fit_order
        del self.ROI
        del self.nref
        del self.reference_data_cube
        del self.reference_data_cube_mask
        del self.empty_test_data_cube_mask

    def test_one(self):
        tracer = jitter.Tracer()
        trace = tracer.center_of_light(self.test_data_cube, self.test_data_cube_mask)
        assert(isinstance(trace, list))
        assert(np.array(trace).shape[0:3] == (1, self.nintegrations, 2))
        assert(np.allclose(np.sum(trace[0][0][0] == 35), 200.0))

    def test_two(self):
        tracer = jitter.Tracer()
        trace, souce_mask, roi, number_of_sources, edge_filter_configuration = \
            tracer.trace_from_edge_filter(self.test_data_cube,
                                          self.test_data_cube_mask)
        assert(isinstance(trace, list))
        assert(np.array(trace).shape[0:3] == (1, self.nintegrations, 2))
        assert(np.allclose(trace[0][0][0], 35.0, atol=0.001))

    #@unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_three(self):
        tracer = jitter.Tracer()
        trace, souce_mask, roi, number_of_sources, edge_filter_configuration = \
            tracer.trace_from_edge_filter(self.test_data_cube,
                                          self.test_data_cube_mask)
        trace_parameters = np.array(tracer.fit_trace(trace, order=self.fit_order))
        assert(trace_parameters.shape == (1, self.nintegrations, self.fit_order+1))
        assert(np.allclose(trace_parameters[0,:,0], 35.0, atol=0.0001))
        assert(np.allclose(trace_parameters[0,:,1], 0.0, atol=0.0001))
        assert(np.allclose(trace_parameters[0,:,2], 0.0, atol=0.0001))

    #@unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_four(self):
        tracer = jitter.Tracer()
        tracer.run_tracer(self.test_data_cube,
                           self.test_data_cube_mask)
        assert(np.allclose(tracer.spectral_traces['sod']['trace'][0][0][0],
                           35.0, atol=0.001))
        assert(np.allclose(np.array(tracer.spectral_traces['sod']['trace_par'])[0,:,0],
                           35.0, atol=0.0001))
        assert(tracer.source_mask.shape == (1, self.nintegrations,
                                           self.nwavelengths, self.nspatial))
    @unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_five(self):
        pp_data_cube = jitter.pre_process_data(self.test_data_cube,
                                               self.test_data_cube_mask,
                                               self.ROI)
        assert(pp_data_cube.shape == (self.nintegrations,)+(200, 200))
        assert(int(np.round(np.sum(pp_data_cube))) == self.nintegrations*255*200)

        pp_data_cube, _ = jitter.pre_process_data(self.test_data_cube,
                                               self.test_data_cube_mask,
                                               self.ROI,
                                               rotation_angle_oversampling=1)
        assert(pp_data_cube.shape == (self.nintegrations,)+(4*360, 4*360))
        assert(int(np.round(np.sum(pp_data_cube))) == self.nintegrations*255*200)

    @unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_six(self):
        pp_data_cube = jitter.pre_process_data(self.test_data_cube,
                                               self.empty_test_data_cube_mask,
                                               self.ROI)
        pp_ref_data_cube = jitter.pre_process_data(self.reference_data_cube,
                                               self.reference_data_cube_mask,
                                               self.ROI)
        shifts = jitter.determine_relative_source_shift(pp_data_cube,
                                                        pp_ref_data_cube)
        assert(np.allclose(shifts[...,1], 1.0))
        assert(np.allclose(shifts[...,0], -1.0))

    @unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_seven(self):
        pp_data_cube, _ = jitter.pre_process_data(self.test_data_cube,
                                               self.empty_test_data_cube_mask,
                                               self.ROI,
                                               rotation_angle_oversampling=1)
        fft_data_cube = jitter.fft_process_data(pp_data_cube)
        assert(pp_data_cube.shape == fft_data_cube.shape)
        fft_image = jitter.fft_process_data(pp_data_cube[0,...])
        assert(np.allclose(fft_data_cube[0,...] - fft_image, 0.0))

    @unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_eight(self):
        pp_data_cube, _ = jitter.pre_process_data(self.test_data_cube,
                                                self.empty_test_data_cube_mask,
                                                self.ROI,
                                                rotation_angle_oversampling=1)
        fft_data_cube = jitter.fft_process_data(pp_data_cube)
        pp_ref_data_cube, _ = jitter.pre_process_data(self.reference_data_cube,
                                                self.reference_data_cube_mask,
                                                self.ROI,
                                                rotation_angle_oversampling=1)
        fft_ref_data_cube = jitter.fft_process_data(pp_ref_data_cube)

        distortions = \
            jitter.determine_relative_rotation_and_scale(fft_data_cube,
                                                          fft_ref_data_cube,
                                                          rotation_angle_oversampling=1)
        assert(np.allclose(distortions[...,0], 0.0))
        assert(np.allclose(distortions[...,1], 1.0))

    @unittest.skipIf(int(os.getenv('TEST_LEVEL', 0)) < 1, 'To expensive, set TEST_LEVEL to run')
    def test_nine(self):
        JD = jitter.JitterDetector()
        JD.run_jitter_detection(self.test_data_cube,
                                self.empty_test_data_cube_mask, self.ROI)



if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJitter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)