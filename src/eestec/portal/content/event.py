from five import grok
from plone.directives import form, dexterity
from Products.CMFCore.interfaces import IDublinCore
from zope.component import adapts
from zope import schema
from zope.interface import implements, alsoProvides


class IEvent(form.Schema):
    """
    """
    deadline = schema.Datetime(
        title=u'Deadline',
        description=u'Deadline to apply to this event',
        required=True,
    )


alsoProvides(IEvent, form.IFormFieldProvider)

class Event(dexterity.Container):
    """
    """
    grok.implements(IEvent)


# TODO: setup subscribers

def event_published(context, event):
    """
    #. Send email to CP list, notifying them that new event was published
    """

    if event.transition:
        if event.transition.id == "publish_event":
            emails.event_published_notify_cp_list(context)
