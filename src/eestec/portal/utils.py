# -*- coding: utf-8 -*-
"""Miscellaneous utility methods used throughout the project."""

from plone import api


def get_portal_from():
    """Build default reply-to address string.

    Use the ``email_from_name`` and ``email_from_name`` site property.
    """
    portal = api.portal.get()
    portal_from = portal.getProperty('email_from_name') + \
         ' <' + portal.getProperty('email_from_address') + '>'
    return portal_from
