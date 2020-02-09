# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.PANIC.
#
# SENAITE.PANIC is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2019-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from senaite.panic import utils


class ResultOutOfRangeAdapter(object):

    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, result, specification):
        """Returns a {'out_of_range': True, 'acceptable': False} dict if the
        result is in panic or {'out_of_range': False} if not in panic
        """
        if utils.is_in_panic(self.analysis, result, specification):
            # Result of out range and unacceptable (in panic)
            return dict(out_of_range=True, acceptable=False)

        # Result in range (might be acceptable)
        return dict(out_of_range=False)
