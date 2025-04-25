import setuptools
import os
import pathlib

def package_files(directory):
    exclude = ['data', 'examples']
    paths = []
    for (path, directories, filenames) in os.walk(directory, topdown=True):
        directories[:] = [d for d in directories if d not in exclude]
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

# The directory containing this file, MUST be RELATIVE
HERE = pathlib.Path(__file__)
HERE = HERE.relative_to(HERE.parent).parent

# The text of the README file
README = (HERE / "README.md").read_text()

extra_files = package_files((HERE/'configuration_files/').as_posix())

scripts =  [(HERE / 'scripts/setup_cascade-jitter.py').as_posix(),]

config = {
    'name': 'CASCADe-jitter',
    'description': 'CASCADe-jitter: Calibration of trAnsit Spectroscopy using CAusal Data jitter detection module.',
    'long_description': README,
    'long_description_content_type': "text/markdown",
    'author': 'Jeroen Bouwman',
    'url': 'https://jbouwman.gitlab.io/CASCADe-jitter/',
    'download_url': 'https://gitlab.com/jbouwman/CASCADe-jitter',
    'author_email': 'bouwman@mpia.de',
    'version': '0.9.7',
    'python_requires': '>=3.9, <3.13',
    'license': 'GNU General Public License v3 (GPLv3)',
    'classifiers': ["Programming Language :: Python :: 3",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Operating System :: OS Independent",
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Astronomy',
                    ],
    'packages': setuptools.find_packages(exclude=("tests_private", "docs", "examples",)),
    'include_package_data': True,
    'package_data': {"": extra_files},
    'install_requires': ['astropy', 'scipy',
                         'numpy', 'configparser', 'jupyter',
                         'scikit-learn', 'matplotlib', 'tqdm', 'seaborn',
                         'pytest', 'scikit-image>=0.19.0', 'sphinx', 'alabaster',
                         'pyfiglet', 'six', 'colorama', 'termcolor',
                         'cython', 'numba','ray[default]',
                         'CASCADe-filtering'
                         ],
    'scripts': scripts,
    'data_files': [('', [(HERE / 'README.md').as_posix(),
                         (HERE / 'LICENSE.txt').as_posix()])]
}

setuptools.setup(**config)
