---
title: Packaging Python Applications
date: '02-10-2011'
time: '22:25'
---
{% extends "post.html" %}

{% block postcontent %}
{% markdown %}
A few days ago, I came across a situation where I needed to create Debian packages for some Python libraries on which our software was dependant on. All these time we were creating and distributing the application as Eggs built using [setuptools](http://pypi.python.org/pypi/setuptools) `setup.py` script. Later on this became a problem since some other applications which we were using were not Python applications and were packaged as `.deb` packages. This situation made us to build `.deb` packages for our Python software as well.

The real challenge here was packaging all the dependencies our Python application has brought in, as most of the dependencies were having only `egg` distributions. Luckily there was an extension to setuptools called [stdeb](https://github.com/astraw/stdeb) which will allow you to generate debian packages using your setup.py script. It'll automatically add the dependencies in the `debian/control` file after searching for the dependencies using `apt-cache`. stdeb will do something like `apt-cache dump | grep <package>` to find whether there is a proper debian package for the dependencies. If they found the correct one in apt-cache, `debian/control` file will be updated with that information. But as I said, most of the dependencies were not packaged as `.deb`. So we downloaded all the dependencies using the `easy_install` command and created `.deb` packages for them using `stdeb`.

I will demonstrate the procedure with the [Voldemort](https://github.com/semk/voldemort) project from my GitHub Repo. The `setup.py` looks like this,

	:::python
	try:
	    from setuptools import setup, find_packages
	except ImportError:
	    from ez_setup import use_setuptools
	    use_setuptools()
	    from setuptools import setup, find_packages

	setup(
	    name='voldemort',
	    version='0.5.0',
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

In this case all the dependencies were lacking `.deb` packages. So, we need to download them using `easy_install`.

	:::bash
	mkdir deps
	easy_install -e -b deps/ "Pygments>=1.4"
	easy_install -e -b deps/ "PyYAML>=3.10"
	easy_install -e -b deps/ "Markdown>=2.0"
	easy_install -e -b deps/ "Jinja2>=2.5"
	ls deps/
	jinja2   markdown pygments pyyaml

Now you need to go to each dependency directory and issue the following command

	:::bash
	python setup.py --command-packages=stdeb.command debianize

That will create a directory named `debian` which contain all the stuffs needed to create a `.deb` package. Now it is upto us to edit the control file and add any additional dependency if needed. To generate the debian package, do

	:::bash
	dpkg-buildpackage -us -uc

Now you can build the main application debs by editing the control file manually since stdeb won't add the dependencies. But you know you have them in your hand :-).
{% endmarkdown %}
{% endblock %}

