# -*- coding: utf-8 -*-
"""Emails sent out when stuff happens to Events."""

from eestec.portal import CP_LIST_ADDRESS
from eestec.portal import BOARD_LIST_ADDRESS
from plone import api
from eestec.portal.utils import get_portal_from


def published_notify_cp_list(event):
    """Send notification email to the CP list, notifying them that a
    new Event has been published.
    """

    body = u"""
Dear CPs,
a new Event has been published on eestec.net:

%(title)s

%(description)s

%(url)s


Best regards,
EESTEC IT Team
"""
    body_values = dict(
        url=event.absolute_url(),
        description=event.description,
        title=event.title,
    )

    api.portal.send_email(
        sender=get_portal_from(),
        recipient=CP_LIST_ADDRESS,
        subject=u'[CP] [EVENTS] %s' % (event.title),
        body=body % body_values)

def created_notify_board(event):
    """Send notification email to the Board list, notifying them that a
    new Event has been created.
    """

    body = u"""
Dear Board,
a new Event has been created on eestec.net:

%(title)s

%(description)s

%(url)s


Best regards,
EESTEC IT Team
"""
    body_values = dict(
        url=event.absolute_url(),
        description=event.description,
        title=event.title,
    )

    api.portal.send_email(
        sender=get_portal_from(),
        recipient=BOARD_LIST_ADDRESS,
        subject=u'[EVENTS][Created] %s' % (event.title),
        body=body % body_values)

def cancelled_notify_board(event):
    """Send notification email to the Board list, notifying them that a
    new Event has been created.
    """

    body = u"""
Dear Board,
an Event has been cancelled on eestec.net:

%(title)s

%(description)s

%(url)s


Best regards,
EESTEC IT Team
"""
    body_values = dict(
        url=event.absolute_url(),
        description=event.description,
        title=event.title,
    )

    api.portal.send_email(
        sender=get_portal_from(),
        recipient=BOARD_LIST_ADDRESS,
        subject=u'[EVENTS][Cancelled] %s' % (event.title),
        body=body % body_values)
