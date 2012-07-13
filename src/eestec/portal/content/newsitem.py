# -*- coding: utf-8 -*-
"""News Item content type. Since we are using the default ATNewsItem type
that comes with Plone we don't really have to do anything here to have it.
So we only have zope.event subscribers in this file.
"""

from eestec.portal import emails
from five import grok
from Products.ATContentTypes.atct import ATNewsItem
from Products.DCWorkflow.interfaces import IAfterTransitionEvent


@grok.subscribe(ATNewsItem, IAfterTransitionEvent)
def news_item_published(context, event):
    """When a News Item is published, send an email to the CP list."""

    # event here is the zope event triggered after a workflow transition is
    # made, not an eestec event ;)
    if event.transition:
        if event.transition.id == "publish":
            emails.news_item.published_notify_cp_list(context)
