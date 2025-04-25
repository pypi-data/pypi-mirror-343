#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from scipy.stats import norm as norm_stats
from cascade_jitter import least_squares


class TestLS(unittest.TestCase):
    def setUp(self):
        # create linear system with RV
        n = 1000
        x1 = norm_stats.rvs(0, 1, size=n)
        x2 = norm_stats.rvs(0, 1, size=n)
        x3 = norm_stats.rvs(0, 1, size=n)
        self.answer = np.array([10.0, 40.0, 0.1])
        self.A = np.column_stack([x1, x2, x3])
        self.b = self.answer[0] * x1 + self.answer[1] * x2 + \
            self.answer[2] * x3
        self.covar = np.identity(n)
        self.delta = np.identity(3)
        self.alpha = 1.e-5

    def tearDown(self):
        del self.answer
        del self.A
        del self.b
        del self.covar
        del self.delta
        del self.alpha

    def test_ols(self):
        # solve linear Eq.
        (P, Perr, _) = least_squares.ols(self.A, self.b)
        for i, (result, error) in enumerate(zip(P, Perr)):
            self.assertAlmostEqual(result, self.answer[i], places=None,
                                   msg=None, delta=1.e4*error)
    def test_ridge(self):
        # solve linear Eq.
        (P, _, _, _, _, _, _) = least_squares.ridge(self.A, self.b, self.covar,
                                                    self.delta, self.alpha)
        for i, result in enumerate(P):
            self.assertAlmostEqual(result, self.answer[i], places=None,
                                   msg=None, delta=0.001)

if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLS)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)