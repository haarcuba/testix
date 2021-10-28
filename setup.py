import setuptools
from distutils.core import setup
LONG_DESCRIPTION =\
"""
Testix is a Mocking framework for Python, meant to be used with [pytest](https://docs.pytest.org/en/latest/).

read the full docs at the [project's homepage](https://github.com/haarcuba/testix).

Testix is special because it allows you to specify what your mock objects do,
and it then enforces your specifications automatically. It also reduces (albeit
not entirely) mock setup. Other frameworks usually have a flow like this:

* setup mock
* let code do something with mock
* assert mock used in correct way

Testix flow is a bit different

* setup "top level" mock objects (`sock` in the following example)
* specify exactly what should happen to them using a scenario

And that's it.  
"""

requires = [ 'pytest>~4.3.0', ]
tests_require = [ 'hypothesis>~4.7.19', 'pytest-asyncio', 'pytest-cov' ]
setup(
    name="testix",
    packages = ["testix",],
    version='7.0.0',
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        ]
)
