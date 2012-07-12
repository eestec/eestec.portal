# -*- coding: utf-8 -*-
"""Catch miscelaneous events and act accordingly."""

from eestec.portal import emails


def news_item_published(context, event):
    """When a News Item is published, send an email to the CP list."""

    # event here is the zope event triggered after a workflow transition is
    # made, not an eestec event ;)
    if event.transition:
        if event.transition.id == "publish":
            emails.news_item.news_item_published_notify_cp_list(context)
