import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-oauthlib",
    version = "0.1",
    author = "Craig Bruce",
    author_email = "craigbruce@gmail.com",
    description = ("An oauth provider built on oauthlib wrapped with Django."),
    license = "BSD",
    keywords = "django oauth provider",
    url = "https://github.com/craigbruce/django-oauthlib",
    packages=['oauth', 'tests'],
    long_description=read('README.rst'),
    requires=[
        'django(==1.4)',
        'oauthlib(>=0.3.0)',
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
)
