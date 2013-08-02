#! /usr/bin/env python

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='voldemort',
    version='0.8.0',
    description='Voldemort is a simple static site generator \
                    using Jinja2 and Markdown templates.',
    long_description=read('README.rst'),
    license='Apache License, Version 2.0',
    keywords='Voldemort Static Site Generator Jinja Jinja2 \
                    Markdown Blog Python',
    author='Sreejith K / K7Computing Pvt Ltd',
    author_email='sreejithemk@gmail.com',
    url='https://github.com/semk/voldemort',
    download_url='https://github.com/semk/voldemort/tarball/master#egg=voldemort-0.8.0',
    install_requires=[
        'Pygments >= 1.4',
        'PyYAML >= 3.10',
        'Markdown >= 2.0',
        'Jinja2 >= 2.5'
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    test_suite='tests',
    entry_points={
        'console_scripts': ['voldemort = voldemort:main']
    },
    include_package_data=True,
    platforms=['any'],
    classifiers=[
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ],
    zip_safe=True
)
