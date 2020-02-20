.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.com/collective/collective.restapi.pfg.svg?branch=master
    :target: https://travis-ci.com/collective/collective.restapi.pfg

.. image:: https://coveralls.io/repos/github/collective/collective.restapi.pfg/badge.svg?branch=master
 :target: https://coveralls.io/github/collective/collective.restapi.pfg?branch=master


======================
collective.restapi.pfg
======================

This is an attempt to build a JSON Schema based endpoint for PloneFormGen forms, so the form can be built in the front-end in the same way that is done for Dexterity fields in plone.restapi.

It also provides a form-data sending endpoint to send the form.

Under the hood it delegates all form processing to PloneFormGen, so it should work as an stardard PloneFormGen.


Documentation
-------------

Not yet :)


Installation
------------

Install collective.restapi.pfg by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.restapi.pfg


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.restapi.pfg/issues
- Source Code: https://github.com/collective/collective.restapi.pfg


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
