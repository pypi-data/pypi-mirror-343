#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:05:19 2022

@author: bouwman
"""

# -*- coding: utf-8 -*-

import unittest
import numpy as np
from cascade_jitter.utilities import create_mask_from_dq
from cascade_jitter.utilities import find
from cascade_jitter.utilities import check_configuration_files
from cascade_jitter.utilities import read_configuration_files


class TesUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_one(self):
        pass

    def test_two(self):
        pass

    def test_three(self):
        pass

    def test_four(self):
        pass


if __name__ == '__main__':
    #  unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TesUtils)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)