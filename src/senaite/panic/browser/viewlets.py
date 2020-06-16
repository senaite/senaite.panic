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

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from senaite.panic import utils

from bika.lims import api
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.permissions import ViewResults
from bika.lims.utils import check_permission


class PanicAlertViewlet(ViewletBase):
    """ Print a viewlet showing panic level alert
    """
    template = ViewPageTemplateFile("templates/panic_alert_viewlet.pt")

    _in_panic = None

    def __init__(self, context, request, view, manager=None):
        super(PanicAlertViewlet, self).__init__(
            context, request, view, manager=manager)
        self.context = context
        self.request = request
        self.view = view

    def is_client_contact(self):
        """Returns whether the current user is a client contact
        """
        return api.get_current_client() is not None

    def available(self):
        """Returns whether the viewlet has to be rendered
        """
        # Do not display if user does not have ViewResults permission
        if check_permission(ViewResults, api.get_object(self.context)):
            return self.in_panic
        return False

    @property
    def in_panic(self):
        """Returns whether the Sample has at least one analysis
        """
        if self._in_panic is None:
            self._in_panic = False
            if IAnalysisRequest.providedBy(self.context):
                self._in_panic = utils.has_analyses_in_panic(self.context)
        return self._in_panic

    @property
    def panic_email_sent(self):
        """Returns whether an email alert has been sent already
        """
        return self.context.getField("PanicEmailAlertSent").get(self.context)

    def render(self):
        if not self.in_panic:
            return ""

        return self.template()
