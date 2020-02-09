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

from bika.lims.content.analysisspec import ResultsRangeDict
from bika.lims.interfaces import ISubmitted
from bika.lims import api
from bika.lims.interfaces.analysis import IRequestAnalysis
from bika.lims.utils import render_html_attributes


def has_analyses_in_panic(sample):
    """Returns whether the sample passed in have at least one analysis for which
    the result is in panic in accordance with the specifications. Only analyses
    in "to_be_verified" status and beyond are considered
    """
    analyses = sample.getAnalyses(full_objects=True)
    for analysis in analyses:
        if ISubmitted.providedBy(analysis) and is_in_panic(analysis):
            return True
    return False


def is_in_panic(analysis, result=None, panic_range=None):
    """Returns whether if the result of the analysis is below the min panic or
    above the max panic
    """
    if result is None:
        result = analysis.getResult()

    # To begin with, the result must be floatable
    result = to_float_or_none(result)
    if result is None:
        return False

    # Get panic min and max
    panic_min, panic_max = get_panic_tuple(analysis, panic_range)

    # Below the min panic?
    if panic_min is not None:
        if result <= panic_min:
            return True

    # Above the max panic?
    if panic_max is not None:
        if result >= panic_max:
            return True

    # Not in panic
    return False


def to_float_or_none(value):
    """Returns the float if the value is floatable. Otherwise, returns None
    """
    if api.is_floatable(value):
        return api.to_float(value)
    return None


def get_panic_tuple(analysis, panic_range=None):
    """Returns a tuple of min_panic and max_panic for the given analysis.
    Resolves each item to None if not found or not valid for the analysis.
    """
    if panic_range is None:
        # Get the panic range directly from the analysis
        panic_range = analysis.getResultsRange() or ResultsRangeDict()

    panic_min = panic_range.get("min_panic", None)
    panic_max = panic_range.get("max_panic", None)
    return tuple(map(to_float_or_none, [panic_min, panic_max]))


def get_image(name, **kwargs):
    """Returns a well-formed image
    :param name: file name of the image
    :param kwargs: additional attributes and values
    :return: a well-formed html img
    """
    if not name:
        return ""
    portal_url = api.get_url(api.get_portal())
    attr = render_html_attributes(**kwargs)
    html = '<img src="{}/++resource++senaite.panic.static/img/{}" {}/>'
    return html.format(portal_url, name, attr)


def get_formatted_panic(analysis, panic_range=None):
    """Returns a string representation of the panic with the result
    """
    panic = get_panic_tuple(analysis, panic_range)
    result = analysis.getResult()
    str_panic = ""
    if result <= panic[0]:
        str_panic = "<= {}".format(panic[0])
    elif result >= panic[1]:
        str_panic = ">= {}".format(panic[1])
    if str_panic:
        return "{} {}".format(str_panic, analysis.getUnit()).strip()
    return ""
