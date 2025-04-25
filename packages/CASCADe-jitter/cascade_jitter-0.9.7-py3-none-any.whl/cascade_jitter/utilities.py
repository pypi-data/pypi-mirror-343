#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:03:54 2022

@author: bouwman
"""
import ast
import numpy as np
import os
import fnmatch
import pathlib
import configparser

__all__=['create_mask_from_dq', 'find', 'check_configuration_files',
         'read_configuration_files']


def check_configuration_files(configuration_file : str, path : pathlib.Path) -> str:
    """
    Check ic configuration file excist.

    Parameters
    ----------
    configuration_file : 'str'
        Configuration file name
    path : 'str' or pathlib.Path
        Path to the configuration file.

    Raises
    ------
    FileNotFoundError
        Error raised if file not found

    Returns
    -------
    file_path : 'str'
        Checked location of configuration file.

    """
    file_path = pathlib.Path(path) / configuration_file
    if not file_path.is_file:
        raise FileNotFoundError(f'The {configuration_file} configuration '
                                'file is not found')
    return str(file_path)


def read_configuration_files(*files):
    """
    Read .ini files using the configparser package.

    Parameters
    ----------
    files : 'list' of 'str'
        List of file names of initialization files to be read to initialize
        an instance of a TSO object.

    Raises
    ------
    ValueError
        An error is raised if the configuration file can not be found.
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str  # make option names case sensitive
    found = parser.read(files)
    if not found:
        raise ValueError('Config file not found!')

    parameters = {}
    section_names = parser.sections()
    for name in section_names:
        parameters.update(parser.items(name))
    for k, v in parameters.items():
        parameters[k] = ast.literal_eval(v)
    return parameters


def find(pattern, path):
    """
    Return  a list of all data files.

    Parameters
    ----------
    pattern : 'str'
        Pattern used to search for files.
    path : 'str'
        Path to directory to be searched.

    Returns
    -------
    result : 'list' of 'str'
        Sorted list of filenames matching the 'pattern' search
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return sorted(result)


def create_mask_from_dq(dq_cube, bits_not_to_flag=[]):
    """
    Create mask from DQ cube.

    Parameters
    ----------
    dq_cube : TYPE
        DESCRIPTION.

    Returns
    -------
    mask : TYPE
        DESCRIPTION.

    Note
    ----
    Standard bit values not to flag are 0, 12 and 14.
    Bit valiue 10 (blobs) is not set by default but can be selected not to
    be flagged in case of problem.
    """
    bits_not_to_flag = bits_not_to_flag
    bits_to_flag = []
    for ibit in range(1, 16):
        if ibit not in bits_not_to_flag:
            bits_to_flag.append(ibit)
    all_flag_values = np.unique(dq_cube)
    bit_select = np.zeros_like(all_flag_values, dtype='int')
    for ibit in bits_to_flag:
        bit_select = bit_select + (all_flag_values & (1 << (ibit - 1)))
    bit_select = bit_select.astype('bool')
    mask = np.zeros_like(dq_cube, dtype='bool')
    for iflag in all_flag_values[bit_select]:
        mask = mask | (dq_cube == iflag)
    return mask