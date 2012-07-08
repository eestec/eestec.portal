# -*- coding: utf-8 -*-
"""Emails related to News Items."""


from eestec.portal import CP_LIST_ADDRESS
from eestec.portal.utils import get_portal_from
from plone import api


def news_item_published_notify_cp_list(news_item):
    """Send notification email to the CP list, notifying them that a new News
    Item has been published.
    """

    body = u"""
Dear CPs,
a new News Item has been published on eestec.net:

%(news_item_title)s

%(description)s

%(news_item_url)s


Best regards,
EESTEC IT Team
"""
    body_values = dict(
        news_item_url=news_item.absolute_url(),
        description=news_item.description,
        news_item_title=news_item.title,
    )

    api.send_email(
        sender=get_portal_from(),
        recipient=CP_LIST_ADDRESS,
        subject=u'[CP] [NEWS] %s' % (news_item.title),
        body=body % body_values)
