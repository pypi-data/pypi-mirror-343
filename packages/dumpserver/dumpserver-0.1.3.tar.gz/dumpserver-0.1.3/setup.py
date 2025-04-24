#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'dumpserver'
DESCRIPTION = 'dumpserver interfaces for python/jython'
URL = 'https://github.com/'
EMAIL = '1449349985@qq.com'
AUTHOR = 'yan wang'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.3'


# What packages are required for this module to be executed?
REQUIRED = ['asgiref==3.5.2', 'blinker==1.4', 'Brotli==1.0.9', 'certifi==2025.1.31', 'cffi==1.17.1', 'click==8.1.8', 'colorama==0.4.6', 'cryptography==36.0.2', 'Flask==2.0.3', 'h11==0.13.0', 'h2==4.1.0', 'hpack==4.0.0', 'hyperframe==6.0.1', 'itsdangerous==2.2.0', 'Jinja2==3.1.6', 'kaitaistruct==0.9', 'ldap3==2.9.1', 'MarkupSafe==2.1.5', 'msgpack==1.0.8', 'passlib==1.7.4', 'pip==24.3.1', 'protobuf==3.19.6', 'publicsuffix2==2.20191221', 'pyasn1==0.6.1', 'pycparser==2.22', 'pydivert==2.1.0', 'pyOpenSSL==22.0.0', 'pyparsing==3.0.9', 'pyperclip==1.8.2', 'ruamel.yaml==0.17.40', 'ruamel.yaml.clib==0.2.8', 'setuptools==75.3.0', 'sortedcontainers==2.4.0', 'tornado==6.4.2', 'urwid==2.1.2', 'Werkzeug==2.0.0', 'wheel==0.45.1', 'wsproto==1.1.0', 'zstandard==0.17.0']

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# # Where the magic happens:
# setup(
#     name=NAME,
#     version=about['__version__'],
#     description=DESCRIPTION,
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     author=AUTHOR,
#     author_email=EMAIL,
#     python_requires=REQUIRES_PYTHON,
#     url=URL,
#     packages=find_packages('src'),
#     # py_modules=['mypackage'],
#     package_dir = {'':'src'},
#     package_data = {
#         '': ['*.html','*.css','*.js','*.json'],
#         'fluke': ['static.*css','templates.*html','locale.*po']
#     },
#     install_requires=REQUIRED,
#     extras_require=EXTRAS,
#     include_package_data=True,
#     license='MIT',
#     classifiers = [
#         # Trove classifiers
#         # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: Implementation :: CPython',
#         'Programming Language :: Python :: Implementation :: PyPy'
#     ],
#     # $ setup.py publish support.
#     cmdclass={
#         'upload': UploadCommand,
#     },
# )


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['fluke'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

