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

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from senaite.panic import messageFactory as _
from zope import schema
from zope.interface import Interface


class IPanicControlPanel(Interface):
    """Control panel settings
    """

    email_subject = schema.TextLine(
        title=_(u"Email alert subject"),
        description=_(
            "Template text for the panic alert email's subject. The accepted "
            "wildcards are: ${sample_id}, {client_sample_id} and ${client_id}"),
        default=_("Some results from Sample ${sample_id} exceeded panic range"),
        required=True,
    )

    email_body = schema.Text(
        title=_(u"Email alert body template"),
        description=_(
            "Template text for the panic alert email's body. The accepted "
            "wildcards are: ${analyses}, ${lab_address}, ${sample_id}, "
            "{client_sample_id}, ${client_id} and ${sample_url}"),
        default=_(
            "Some results from the Sample ${sample_id} exceeded the panic "
            "levels:\n\n${analyses}\n\n--\n${lab_address}"),
        required=True,
    )


class PanicControlPanelForm(RegistryEditForm):
    schema = IPanicControlPanel
    schema_prefix = "senaite.panic"
    label = _("SENAITE PANIC Settings")


QueueControlPanelView = layout.wrap_form(PanicControlPanelForm,
                                         ControlPanelFormWrapper)
