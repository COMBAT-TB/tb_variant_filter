# -*- coding: utf-8 -*-

from distutils.core import setup

from setuptools import find_packages

classifiers = """
Development Status :: 3 - Alpha
Environment :: Console
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
Intended Audience :: Science/Research
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
Programming Language :: Python :: 3.7
Operating System :: POSIX :: Linux
""".strip().split('\n')

setup(
    name='tb_variant_filter',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/pvanheus/tb_variant_filter',
    license='GPLv3',
    author='Peter van Heusden',
    author_email='pvh@sanbi.ac.za',
    description='This tool offers multiple options for filtering variants (in VCF files, relative to M. tuberculosis H37Rv).',
    keywords='Salmonella enterica Heidelberg Enteritidis SNP kmer subtyping Aho-Corasick',
    classifiers=classifiers,
    package_dir={'tb_variant_filter': 'tb_variant_filter'},
    install_requires=[
        'lxml>=4.3.2',
        'pandas>=0.24.2',
        'requests>=2.21.0'
        'py2neo>=4.2.0',
        'pytest>=4.3.1'
    ],
    extras_require={
        'test': ['pytest>=4.3.1',],
    },
    entry_points={
        'console_scripts': [
            'tb_variant_report=tb_variant_filter.cli:main',
        ],
    }
)