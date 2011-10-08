try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='voldemort',
    version='0.6.5',
    description='Voldemort is a simple static site generator\
                    using Jinja2 and markdown templates.',
    author='Sreejith K / K7Computing Pvt Ltd',
    author_email='sreejithemk@gmail.com',
    url='http://www.foobarnbaz.com',
    install_requires=[
        'Pygments >= 1.4',
        'PyYAML >= 3.10',
        'Markdown >= 2.0',
        'Jinja2 >= 2.5'
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    test_suite='tests',
    scripts = ['scripts/voldemort'],
    include_package_data=True,
    zip_safe=True,
)
