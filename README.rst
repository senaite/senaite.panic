Panic level alerts for SENAITE LIMS
===================================

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
-----

This add-on enables panic level alerts for `SENAITE LIMS`_ by means of the
integration of panic ranges in Analysis Specifications. `senaite.panic`_ adds
two sub-fields *min_panic* and *max_panic*: when the result of an analysis falls
outside the valid range and below *min_panic* or above *max_panic*, a warning
message is displayed next to the analysis and an informative panel in Sample's
view as well. From this informative panel, lab manager can easily send an e-mail
notification to the client contact, as well as to other key personnel.


Documentation
-------------

* https://senaitepanic.readthedocs.io


Contribute
----------

We want contributing to SENAITE.QUEUE to be fun, enjoyable, and educational
for anyone, and everyone. This project adheres to the `Contributor Covenant`_.

By participating, you are expected to uphold this code. Please report
unacceptable behavior.

Contributions go far beyond pull requests and commits. Although we love giving
you the opportunity to put your stamp on SENAITE.QUEUE, we also are thrilled
to receive a variety of other contributions.

Please, read `Contributing to senaite.panic document`_.

If you wish to contribute with translations, check the project site on `Transifex`_.


Feedback and support
--------------------

* `Community site`_
* `Gitter channel`_
* `Users list`_


License
-------

**SENAITE.PANIC** Copyright (C) 2019-2020 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2`_ as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.


.. Links

.. _SENAITE LIMS: https://www.senaite.com
.. _senaite.panic: https://pypi.org/project/senaite.panic
.. _Contributor Covenant: https://github.com/senaite/senaite.panic/blob/master/CODE_OF_CONDUCT.md
.. _Contributing to senaite.panic document: https://github.com/senaite/senaite.panic/blob/master/CONTRIBUTING.md
.. _Transifex: https://www.transifex.com/senaite/senaite-panic
.. _Community site: https://community.senaite.org/
.. _Gitter channel: https://gitter.im/senaite/Lobby
.. _Users list: https://sourceforge.net/projects/senaite/lists/senaite-users
.. _GNU General Public License version 2: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
