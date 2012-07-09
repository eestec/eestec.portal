from rwproperty import getproperty, setproperty

from five import grok
from zope import schema
from zope.interface import implements, alsoProvides
from zope.component import adapts

from plone.directives import form, dexterity

from Products.CMFCore.interfaces import IDublinCore


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

    def __init__(self, context):
        self.context = context
