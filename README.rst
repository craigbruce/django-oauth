django-oauthlib
===============

.. note::
	Given a flurry of other django oauth related projects having cropped up. I suggest you try one of them out. `Django OAuth Toolkit <https://github.com/evonove/django-oauth-toolkit>`_ looks very promising, for example.


An OAuth provider built on `oauthlib <https://github.com/idan/oauthlib/>`_ wrapped with Django. Currently targeting OAuth 1.0. This project is under (slow) development.

.. image:: https://travis-ci.org/craigbruce/django-oauth.png?branch=master
        :target: https://travis-ci.org/craigbruce/django-oauth

Installation
------------

Direct from GitHub using ``pip install git+https://github.com/craigbruce/django-oauthlib.git#egg=django-oauthlib``. django-oauthlib will be made available on PyPI after more development.

In your Django ``settings.py`` add ``oauth`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'oauth',
        )

Usage
-----

To follow.

Tests
-----

Create a virtualenv first, then::

    pip install -U -r requirements.txt
    cd tests
    ./run_tests.sh

License
-------

django-oauthlib is licensed under the BSD license, see LICENSE.
