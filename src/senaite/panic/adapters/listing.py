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

import collections

from bika.lims.permissions import ViewResults
from senaite.core.listing.interfaces import IListingView
from senaite.core.listing.interfaces import IListingViewAdapter
from senaite.panic import is_installed
from senaite.panic import messageFactory as _
from senaite.panic import utils
from zope.component import adapts
from zope.interface import implements

from bika.lims import api


class AnalysisSpecificationListingViewAdapter(object):
    """Adapts the Analysis Specifications listing view by adding the columns
    'min_panic' and 'max_panic' and making them editable fields
    """
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        # Don't do anything if senaite.panic is not installed
        # This is necessary for subscribers
        if not is_installed():
            return

        # Add the columns
        new_columns = collections.OrderedDict((
            ("min_panic", {
                "title": _("Panic < Min"),
                "sortable": False}),
            ("max_panic", {
                "title": _("Panic > Max"),
                "sortable": False}),
        ))
        self.listing.columns.update(new_columns)

        # Apply the columns to all review_states
        keys = self.listing.columns.keys()
        map(lambda rv: rv.update({"columns": keys}), self.listing.review_states)

    def folder_item(self, obj, item, index):
        # Don't do anything if senaite.panic is not installed
        # This is necessary for subscribers
        if not is_installed():
            return item

        obj = api.get_object(obj)
        keyword = obj.getKeyword()
        spec = self.listing.specification.get(keyword, {})

        # Set the values in the listing
        item["min_panic"] = spec.get("min_panic", "")
        item["max_panic"] = spec.get("max_panic", "")

        # Make the fields editable
        item["allow_edit"].extend(["min_panic", "max_panic"])

        return item


class AnalysesListingViewAdapter(object):
    """Adapts the Analyses listing view by placing a severe warn icon when the
    result for a given analysis is in panic
    """
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        # Don't do anything if senaite.panic is not installed
        # This is necessary for subscribers
        if not is_installed():
            return

    def folder_item(self, obj, item, index):
        # Don't do anything if senaite.panic is not installed
        # This is necessary for subscribers
        if not is_installed():
            return item

        if not self.listing.has_permission(ViewResults, obj):
            # Users without permissions to see the result should not be able
            # to see if the result is in panic neither
            return

        obj = api.get_object(obj)
        if utils.is_in_panic(obj):
            # Place a severe warning icon next to the result
            img = utils.get_image("panic.png", title=_("Panic result"))
            self.listing._append_html_element(item, element="Result", html=img)

        return item
