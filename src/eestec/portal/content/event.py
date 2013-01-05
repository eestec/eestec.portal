# -*- coding: utf-8 -*-
"""The event content type. Dexterity is awesome!"""

from Products.CMFCore.interfaces import IActionSucceededEvent
from zope.lifecycleevent import IObjectCreatedEvent
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
def event_transitioned(context, event):
    """
    Handle actions on event workflow states change.
    Supported transitions: publish and cancel.

    Example: send an email to International Board if an event is cancelled
    """
    if event.action == 'publish':
        emails.event.published_notify_cp_list(context)
    if event.action == 'cancel':
        emails.event.cancelled_notify_board(context)


@grok.subscribe(Event, IObjectCreatedEvent)
def event_created(context, event):
    """
    Send email to Board list, notifying them that the new event was created
    """
    emails.event.created_notify_board(context)
