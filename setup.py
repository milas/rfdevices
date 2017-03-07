import os
import sys

from setuptools import setup, find_packages

import versioneer

# try to convert from markdown to RST but don't blow-up if we can't
readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
try:
    from pypandoc import convert
    readme = convert(readme_path, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()

install_requires = ['Adafruit-GPIO']
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    # need backport typing package
    install_requires.append('typing')


setup(
    name='rfdevices',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=install_requires,
    scripts=['scripts/rfsend'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={
        'rfdevices': ['protocols/*.conf']
    },
    author='Milas Bowman',
    author_email='milasb@gmail.com',
    description='Control household RF devices with low-cost GPIO modules',
    long_description=readme,
    url='https://github.com/milas/rfdevices',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Home Automation',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
    keywords=[
        'rpi',
        'raspberry',
        'raspberry pi',
        'adafruit',
        'beaglebone',
        'rf',
        'gpio',
        'radio',
        '433',
        '433mhz',
        '315',
        '315mhz'
    ]
)
