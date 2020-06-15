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

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from email.Utils import formataddr
from plone.app.layout.globals.interfaces import IViewView
from plone.memoize import view
from senaite.panic import logger
from senaite.panic import messageFactory as _
from senaite.panic import utils
from zope.interface import implements

from bika.lims import api
from bika.lims.api import user as api_user
from bika.lims.browser import BrowserView
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.utils import encode_header
from bika.lims.utils import t as _t


class EmailPopupView(BrowserView):
    implements(IViewView)

    template = ViewPageTemplateFile("templates/panic_alert_email.pt")

    _marker = object()
    _sample = _marker

    def __call__(self):
        # If sample is not valid, do not render
        if self.sample is None:
            return "Context is not a sample or no sample uid specified"

        # If the email for panic levels has been submitted, send the email
        if "email_popup_submit" in self.request:
            return self.send_panic_email()

        # Return the template
        return self.template()

    @property
    def back_url(self):
        return api.get_url(self.sample)

    @property
    def sample(self):
        if self._sample == self._marker:
            # Maybe current context is a Sample?
            if IAnalysisRequest.providedBy(self.context):
                self._sample = self.context
                return self._sample

            # Try with the uid
            uid = self.request.get("uid")
            sample = self.get_object_by_uid(uid)
            if sample and IAnalysisRequest.providedBy(sample):
                self._sample = sample
            else:
                self._sample = None

        return self._sample

    @view.memoize
    def get_object_by_uid(self, uid):
        if uid and uid != "0" and api.is_uid(uid):
            return api.get_object_by_uid(uid)
        return None

    @property
    def recipients(self):
        """Returns the recipients the notification email has to be sent to
        """
        contacts = self.get_client_contacts(self.sample)
        contacts.extend(self.get_other_contacts(self.sample))
        contacts = list(set(contacts))

        # Generate the recipients
        recipients = map(lambda con: self.get_recipient(con), contacts)
        recipients = filter(None, recipients)

        # Include the client in the recipients list
        client = self.sample.getClient()
        client_email = client.getEmailAddress()
        if client_email:
            recipients.append({
                "uid": api.get_uid(client),
                "name": api.get_title(client),
                "email": client_email,
            })
        return recipients

    @property
    def formatted_recipients(self):
        out = list()
        for recipient in self.recipients:
            name = recipient["name"]
            email = recipient["email"]
            out.append("%s <%s>" % (name, email))
        return ', '.join(out)

    @property
    def subject(self):
        """Returns the subject of the email
        """
        client = self.sample.getClient()
        email_subject = api.get_registry_record("senaite.panic.email_subject")
        mapping = {
            "sample_id": api.get_id(self.sample),
            "client_id": client.getClientID(),
            "client_sample_id": self.sample.getClientSampleID(),
        }
        return _t(_(email_subject, mapping=mapping))

    @property
    def body(self):
        """Returns the body message of the email
        """
        setup = api.get_setup()
        laboratory = setup.laboratory
        lab_address = "\n".join(laboratory.getPrintAddress())
        analyses = map(self.to_str, self.get_analyses_in_panic(self.sample))
        analyses = "\n-".join(analyses)
        client = self.sample.getClient()

        # TODO more mappings here (custom body)!
        email_body = api.get_registry_record("senaite.panic.email_body")
        mapping = {
            "sample_id": api.get_id(self.sample),
            "analyses": analyses,
            "lab_address": lab_address,
            "client_id": client.getClientID(),
            "client_sample_id": self.sample.getClientSampleID(),
            "sample_url": api.get_url(self.sample),
        }
        return _t(_(email_body, mapping=mapping))

    def get_client_contacts(self, sample):
        """Returns a list with the primary contacts from the client side
        """
        contacts = sample.getCCContact() or []
        contacts.insert(0, sample.getContact())
        return filter(None, contacts)

    def get_other_contacts(self, sample):
        """Returns a list with additional contacts the alert has to be sent to
        """
        contacts = set()
        contacts.add(api.get_user_contact(api_user.get_user()))

        # Get the responsibles of departments
        in_panic = self.get_analyses_in_panic(sample)
        departments = map(lambda an: an.getDepartment(), in_panic)
        managers = map(lambda dept: dept.getManager(), departments)
        for manager in managers:
            if manager:
                contacts.add(manager)
        return list(contacts)

    def get_analyses_in_panic(self, sample):
        """Returns the analyses found in panic for the given sample
        """
        for analysis in sample.getAnalyses(full_objects=True):
            if utils.is_in_panic(analysis):
                yield analysis

    def get_recipient(self, contact):
        """Returns a dict representing an email recipient
        """
        if not contact:
            return None
        contact_obj = api.get_object(contact)
        email = contact_obj.getEmailAddress()
        if not email:
            return None
        return {'uid': api.get_uid(contact_obj),
                'name': contact_obj.Title(),
                'email': email}

    def to_str(self, analysis):
        """Returns a string representation of the analysis
        """
        return "{} ({}) {}".format(
            api.get_title(analysis),
            analysis.getKeyword(),
            utils.get_formatted_panic(analysis)).strip()

    def send_panic_email(self):
        # Send an alert email
        setup = api.get_setup()
        laboratory = setup.laboratory
        subject = self.request.get('subject')
        to = self.request.get('to')
        body = self.request.get('email_body')
        body = "<br/>".join(body.split("\r\n"))
        mime_msg = MIMEMultipart('related')
        mime_msg['Subject'] = subject
        mime_msg['From'] = formataddr(
            (encode_header(laboratory.getName()),
             laboratory.getEmailAddress()))
        mime_msg['To'] = to
        msg_txt = MIMEText(safe_unicode(body).encode('utf-8'), _subtype='html')
        mime_msg.preamble = 'This is a multi-part MIME message.'
        mime_msg.attach(msg_txt)
        try:
            host = api.get_tool("MailHost")
            host.send(mime_msg.as_string(), immediate=True)
        except Exception, msg:
            sample_id = api.get_id(self.sample)
            logger.error("Panic level email %s: %s" % (sample_id, str(msg)))
            message = _("Unable to send an email to alert client "
                        "that some results exceeded the panic levels")
            message = "{}: {}".format(message, str(msg))

            return self.redirect(self.back_url, message, "warning")

        # Store this fact in the Sample object
        self.sample.getField("PanicEmailAlertSent").set(self.sample, True)

        message = _("Panic notification email sent")
        return self.redirect(self.back_url, message)

    def redirect(self, redirect_url=None, message=None, level="info"):
        """Redirect with a message
        """
        if redirect_url is None:
            redirect_url = self.back_url
        if message is not None:
            self.add_status_message(message, level)
        return self.request.response.redirect(redirect_url)

    def add_status_message(self, message, level="info"):
        """Set a portal status message
        """
        return self.context.plone_utils.addPortalMessage(message, level)
