
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'adata',
    version = '0.0.1',
    description = 'A data framework',
    long_description = long_description,
    url = 'https://github.com/txemavs/adata',
    author = 'Txema Vicente',
    author_email = 'txema@nabla.net',
    license = 'MIT',

    keywords = 'frozen wx framework',
    classifiers = [
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    packages = find_packages(exclude=['modules', 'docs', 'tests*']),
    install_requires=[],
    package_data={
        'config': ['config.ini'],
    },
    entry_points={
        'console_scripts': [
            'adata=adata_run:main',
        ],
    },
)
