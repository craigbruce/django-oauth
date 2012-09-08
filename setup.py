import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(
    name='django-{{ app_name }}',
    version=__import__('{{ app_name }}').__version__,
    author='Craig Bruce',
    author_email='craigbruce@gmail.com',
    description=u' '.join(__import__('{{ app_name }}').__doc__.splitlines()).strip(),
    license='BSD',
    keywords='django oauth provider',
    url='https://github.com/craigbruce/django-oauthlib',
    packages=find_packages(),
    include_package_data=True,
    long_description=read_file('README.rst'),
    install_requires = ['docutils>=0.3'],
    test_suite="runtests.runtests",
    zip_safe=False,
    requires=[
        'django(>=1.4)',
        'oauthlib(>=0.3.0)',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
