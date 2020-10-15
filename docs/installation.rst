Installation
============

Add ``senaite.panic`` in the eggs section of your buildout:

.. code-block::

  eggs =
      senaite.lims
      senaite.panic


Run ``bin/buildout`` afterwards.

Once buildout finishes, start the instance, login with a user with "Site
Administrator" privileges and activate the add-on:

http://localhost:8080/senaite/prefs_install_products_form

.. note:: It assumes you have a SENAITE zeo client listening to port 8080
