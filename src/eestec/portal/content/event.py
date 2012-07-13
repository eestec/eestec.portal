# -*- coding: utf-8 -*-
"""The event content type. Dexterity is awesome!"""

from Products.CMFCore.interfaces import IActionSucceededEvent
from eestec.portal import emails
from five import grok
from plone.directives import form, dexterity
from zope import schema
from zope.interface.declarations import alsoProvides


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


@grok.subscribe(Event, IActionSucceededEvent)
def event_published(context, event):
    """
    Send email to CP list, notifying them that new event was published
    """
    if event.action == 'publish':
        emails.event.published_notify_cp_list(context)
