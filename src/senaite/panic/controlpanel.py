from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from senaite.panic import messageFactory as _
from zope import schema
from zope.interface import Interface


class IPanicControlPanel(Interface):
    """Control panel settings
    """

    email_body = schema.Text(
        title=_(u"Email alert body template"),
        description=_(
            "Template text for the panic alert email's body. The accepted "
            "wildcards are: ${analyses}, ${lab_address} and ${sample_id}"),
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
