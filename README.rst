*Panic level alerts for SENAITE LIMS*
=====================================

.. image:: https://img.shields.io/pypi/v/senaite.panic.svg?style=flat-square
    :target: https://pypi.python.org/pypi/senaite.panic

.. image:: https://img.shields.io/travis/senaite/senaite.panic/master.svg?style=flat-square
    :target: https://travis-ci.org/senaite/senaite.panic

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.panic.svg?style=flat-square
    :target: https://github.com/senaite/senaite.panic/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.panic.svg?style=flat-square
    :target: https://github.com/senaite/senaite.panic/issues

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
=====

This package enables panic level alerts in SENAITE by means of the integration
of panic ranges in Analysis Specifications. Two additional fields *min_panic*
and *max_panic* are added, so when the result of an analysis falls outside the
valid range and below *min_panic* or *max_panic*, a warning message is displayed
next to the analysis and an informative panel in Sample's view as well. From
this informative panel, lab manager can easily send an e-mail notification to
the client contact, as well as to other key personnel.


Installation
============

Add *senaite.panic* in the eggs section of your buildout:

.. code-block::

  eggs =
      senaite.lims
      senaite.panic


and run *bin/buildout*. Install *senaite.panic* add-on on "Setup > Add-ons".

Contribute
==========

We want contributing to SENAITE.PANIC to be fun, enjoyable, and educational
for anyone, and everyone. This project adheres to the `Contributor Covenant
<https://github.com/senaite/senaite.panic/blob/master/CODE_OF_CONDUCT.md>`_.

By participating, you are expected to uphold this code. Please report
unacceptable behavior.

Contributions go far beyond pull requests and commits. Although we love giving
you the opportunity to put your stamp on SENAITE.PANIC, we also are thrilled
to receive a variety of other contributions.

Please, read `Contributing to senaite.panic document
<https://github.com/senaite/senaite.panic/blob/master/CONTRIBUTING.md>`_.

If you wish to contribute with translations, check the project site on
`Transifex <https://www.transifex.com/senaite/senaite-queue/>`_.


Feedback and support
====================

* `Community site <https://community.senaite.org/>`_
* `Gitter channel <https://gitter.im/senaite/Lobby>`_
* `Users list <https://sourceforge.net/projects/senaite/lists/senaite-users>`_


License
=======

**SENAITE.PANIC** Copyright (C) 2019-2020 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2
<https://github.com/senaite/senaite.panic/blob/master/LICENSE>`_ as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
