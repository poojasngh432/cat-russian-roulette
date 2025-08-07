from setuptools import setup
import os

APP = ['main.py']
DATA_FILES = ['assets']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['pygame'],
    'includes': [],
    'plist': {
        'CFBundleName': 'CatRussianRoulette',
        'CFBundleShortVersionString': '1.0.0',
    },
    'site_packages': True,  # Include all site packages
    'semi_standalone': False,  # Create truly standalone app
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)