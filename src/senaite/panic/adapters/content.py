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

from Products.Archetypes.Widget import BooleanWidget
from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from senaite.panic import ISenaitePanicLayer
from senaite.panic import messageFactory as _
from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.fields import ExtBooleanField
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.interfaces import IAnalysisSpec
from bika.lims.validators import \
    AnalysisSpecificationsValidator as BaseValidator
from bika.lims.validators import get_record_value


class AnalysisRequestSchemaExtender(object):
    """Schema Extender for Sample objects
    """
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    # Modify the schema only if senaite.panic is installed
    layer = ISenaitePanicLayer

    custom_fields = [
        # Stores if a panic email has been sent
        ExtBooleanField(
            "PanicEmailAlertSent",
            default=False,
            widget=BooleanWidget(
                visible=False,
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.custom_fields


def fiddle_panic_subfields(schema):
    # Add panic alert sub fields and labels
    labels = collections.OrderedDict((
        ("min_panic", _("Min panic")),
        ("max_panic", _("Max panic")),
    ))
    for label in labels.keys():
        if label not in schema["ResultsRange"].subfields:
            schema["ResultsRange"].subfields += (label,)

    schema["ResultsRange"].subfield_labels.update(labels)
    return schema


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    # Modify the schema only if senaite.panic is installed
    layer = ISenaitePanicLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Add panic alert sub fields and labels
        return fiddle_panic_subfields(schema)


class AnalysisSpecSchemaModifier(object):
    adapts(IAnalysisSpec)
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    # Modify the schema only if senaite.panic is installed
    layer = ISenaitePanicLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Add panic alert sub fields and labels
        schema = fiddle_panic_subfields(schema)

        # Set the sub field validators
        validator = AnalysisSpecificationsValidator()
        validators = {
            "min_panic": validator,
            "max_panic": validator,
        }
        schema["ResultsRange"].subfield_validators.update(validators)
        return schema


class AnalysisSpecificationsValidator(BaseValidator):
    """Min panic value must be below min value
       Max panic value must be above max value
       Values must be numeric
    """
    implements(IValidator)
    name = "senaite_panic_analysisspecs_validator"

    def validate_service(self, request, uid):
        """Validates the specs values from request for the service uid. Returns
        a message if the validation failed
        """
        spec_min = get_record_value(request, uid, "min")
        spec_max = get_record_value(request, uid, "max")
        min_panic = get_record_value(request, uid, "min_panic")
        max_panic = get_record_value(request, uid, "max_panic")

        if not min_panic and not max_panic:
            # Neither min_panic nor max_panic values are set, dismiss
            return None

        if min_panic:
            if not api.is_floatable(min_panic):
                return _("'{}' value must be numeric or empty").format(
                    _("Min panic"))

            if api.to_float(min_panic) > api.to_float(spec_min):
                return _("'{}' value must be below '{}' or empty").format(
                    _("Min panic"), _("Min"))

        if max_panic:
            if not api.is_floatable(max_panic):
                return _("'{}' value must be numeric or empty").format(
                    _("Max panic"))

            if api.to_float(max_panic) < api.to_float(spec_max):
                return _("'{}' value must be above '{}' or empty").format(
                    _("Max panic"), _("Max"))

        return None


validation.register(AnalysisSpecificationsValidator())
