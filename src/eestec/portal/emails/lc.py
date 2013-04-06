# -*- coding: utf-8 -*-
"""Emails sent out when stuff happens to LCs."""

from plone import api


def lc_created_notify_cp(lc, user):
    """Send notification email to the CP of the newly created LC with log-in
    details.
    """

    body = u"""
Welcome to the EESTEC portal!

You have received this email, because your LC was added to our database.

Use the following URL to set your password:

username : %(username)s
URL : %(portal_url)s/mail_password_form?userid=%(username)s

Best regards,
EESTEC IT Team
"""
    body_values = dict(
        username=user.id,
        portal_url=api.portal.get().absolute_url(),
    )

    api.portal.send_email(
        sender="admin@mysite.com",
        body=body % body_values,
        recipient=user.getProperty('email'),
        subject=u'[EESTEC Website] registration completed',
    )
