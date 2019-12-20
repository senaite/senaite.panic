
import plone.protect
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.globals.interfaces import IViewView
from plone.memoize import view
from senaite.panic import utils
from zope.interface import implements

from bika.lims import api
from bika.lims.api import user as api_user
from bika.lims.browser import BrowserView
from bika.lims.interfaces import IAnalysisRequest


class EmailPopupView(BrowserView):
    implements(IViewView)

    template = ViewPageTemplateFile("templates/panic_alert_email.pt")

    _marker = object()
    _sample = _marker

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)

        # If sample is not valid, do not render
        if self.sample is None:
            return "Context is not a sample or no sample uid specified"

        # Return the template
        return self.template()

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
        txt = "Some results from Sample ${sample_id} exceeded panic range"
        return self.context.translate(txt, mapping={
                  "sample_id": api.get_id(self.sample), })

    @property
    def body(self):
        """Returns the body message of the email
        """
        setup = api.get_setup()
        laboratory = setup.laboratory
        lab_address = "\n".join(laboratory.getPrintAddress())

        # TODO more mappings here (custom body)!
        return self.context.translate(
            "Some results from the Sample ${sample_id} "
            "exceeded the panic levels that may indicate an "
            "imminent life-threatening condition."
            "\n\n${lab_address}",
            mapping={
            'sample_id': api.get_id(self.sample),
            'lab_address': lab_address
        })

    def get_client_contacts(self, sample):
        """Returns a list with the primary contacts from the client side
        """
        contacts = [sample.getContact(), sample.getCCContact()]
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
