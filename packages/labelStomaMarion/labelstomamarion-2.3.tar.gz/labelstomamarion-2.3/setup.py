#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages, Command
from sys import platform as _platform
from shutil import rmtree
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'labelStomaMarion'
REQUIRES_PYTHON = '>=3.12'
REQUIRED_DEP = ['pyqt5', 'lxml','imutils==0.5.4','tqdm==4.67.1','XlsxWriter==3.2.3','six==1.17.0','numpy==2.2.4','progressbar2==3.47.0','scikit_learn==1.6.1','pandas==2.2.3','xlwt==1.3.0','sip==1.17.0']
about = {}

with open(os.path.join(here, 'libs', '__init__.py')) as f:
    exec(f.read(), about)

readme = ""
#with open('README.md') as readme_file:
#    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# OS specific settings
SET_REQUIRES = []
if _platform == "linux" or _platform == "linux2":
   # linux
   print('linux')
elif _platform == "darwin":
   # MAC OS X
   SET_REQUIRES.append('py2app')

required_packages = find_packages()
required_packages.append('labelStomaMarion')
required_packages.append('notebooks')
required_packages.append('predict')
required_packages.append('fichs')
APP = [NAME + '.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'resources/icons/app.icns'
}

class UploadCommand(Command):
    """Support setup.py upload."""

    description=readme + '\n\n' + history,

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
            self.status('Fail to remove previous builds..')
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag -d v{0}'.format(about['__version__']))
        os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()


setup(
    app=APP,
    name=NAME,
    version="2.3",
    description="labelStoma is a graphical tool for using and creating detection models",
    long_description="labelStoma is a graphical tool for using and creating detection models",
    author="Angela Casado",
    author_email='angela.casado@unirioja.es',
    #url='https://github.com/ancasag/labelStoma',
    python_requires=REQUIRES_PYTHON,
    package_dir={'labelStomaMarion': '.'},
    packages=required_packages,
    entry_points={
        'console_scripts': [
            'labelStomaMarion=labelStomaMarion.labelStomaMarion:main'
        ]
    },
    include_package_data=True,
    install_requires=REQUIRED_DEP,
    license="MIT license",
    zip_safe=False,
    keywords='labelStomaMarion detection deeplearning',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    package_data={'data/predefined_classes.txt': ['data/predefined_classes.txt'],'notebooks': ['notebooks/*.ipynb'],'fichs/vocEstomas.names': ['fichs/vocEstomas.names'],'fichs/yolov3Estomas.cfg': ['fichs/yolov3Estomas.cfg'],'resources/strings/strings.properties':['resources/strings/strings.properties'],'resources/strings/strings-zh-CN.properties':['resources/strings/strings-zh-CN.properties'],'resources/strings/strings-zh-TW.properties':['resources/strings/strings-zh-TW.properties']},
    options={'py2app': OPTIONS},
    setup_requires=SET_REQUIRES,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    }
)
