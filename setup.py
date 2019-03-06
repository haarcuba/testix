import setuptools
from distutils.core import setup
LONG_DESCRIPTION =\
"""
# TESTIX

Testix is a Mocking framework for Python.

## Credit Where it's due
Testix started as a re-implementation of ideas from the Voodoo-Mock unit-testing framework (http://sourceforge.net/projects/voodoo-mock), which also supports C++ unit testing. Check it out. Since then it has evolved some different traits though.

## License
This software is free software, and is distributed under the GNU General Public License version 3.0.
See the COPYING file for details.


## Installation
With `pip`:

    $ pip install testix

## Python 3

Testix has been tried with Python 3, but it may work with Python 2 as well.

## How to use it

TBD - for the time being, look at the examples.

Testix is intended to be used with `unittest`, the standrad Python unit testing framework.
If you clone this repository you can run the examples like so

    $ python3 -m unittest examples/tests/test_*.py

Or, if you have [`rake`](http://rake.rubyforge.org/) you can run

    $ rake examples

Enjoy!
"""

requires = [ 'pytest>~4.3.0', ]
tests_require = [ 'hypothesis>~4.7.19' ]
setup(
    name="testix",
    packages = ["testix", "examples", "examples.tests"],
    version='3.0.1',
    description = "Mocking framework Python with *exact* Scenarios",
    author = "Yoav Kleinberger",
    author_email = "haarcuba@gmail.com",
    url = "https://github.com/haarcuba/testix",
    keywords = ["mock", "mocking", "unittest", "python", "unit testing"],
    install_requires=requires,
    long_description = LONG_DESCRIPTION,
    extras_require={
        'testing': tests_require,
    },
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        ]
)
