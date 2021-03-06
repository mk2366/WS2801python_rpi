"""
This file was copied from:
https://github.com/pypa/sampleproject/blob/master/setup.py
and modified to fit needs
"""


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='WS2801_RPI',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version='1.0.0',

    # MK: included as descibed on https://pypi.python.org/pypi/setuptools_scm
    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='Conecting WS2801 LED strip to Raspberry Pi',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mk2366/WS2801python_rpi',

    # Author details
    author='Markus Kupke',
    author_email='kupkemarkus@gmail.com',

    # Choose your license
    license='GNU GENERAL PUBLIC LICENSE',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Education',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='RaspberryPi WS2801 DIY',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # MK: included according to http://nose2.readthedocs.io/en/latest/usage.html
    # test_suite='nose2.collector.collector',
    # MK: according to http://python-packaging.readthedocs.io/en/latest/testing.html more compatible than nose2
    test_suite='nose.collector',
    tests_require=['nose'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["WS2801_RPI"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['spidev', 'setuptools'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)
