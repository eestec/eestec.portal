#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Products.CMFCore.interfaces import ISiteRoot
from five import grok
from plone import api
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form import button
from zope import schema


class ILC(form.Schema, IImageScaleTraversable):
    """LC field specification."""

    title = schema.TextLine(
        title=u"City",
        description=u"City name of the LC",
    )


class LC(dexterity.Container):
    """EESTEC Local Committee."""
    grok.implements(ILC)

    def full_title(self):
        """Return full name of LC, for example: JLC Antwerp."""
        if not self.id:
            return ''

        state = api.content.get_state(self)
        if state == 'inactive':
            state = '(inactive)'
        if state.lower() == 'observer':
            state = state.title()
        else:
            state = state.upper()
        return u'%s %s' % (state, self.title)


class INewLCForm(form.Schema):
    """Define form fields for adding new LC."""

    title = schema.TextLine(
        title=u"City",
        description=u"City name of a LC",
    )

    # CP == Contact Person
    cp_name = schema.TextLine(
        title=u"CP name",
        description=u"Contact person name",
    )

    cp_surname = schema.TextLine(
        title=u"CP surname",
        description=u"Contact person surname",
    )

    cp_username = schema.TextLine(
        title=u"CP username",
        description=u"Contact person username",
    )

    cp_email = schema.TextLine(
        title=u"CP email",
        description=u"Contact person email",
    )


class NewLCForm(form.SchemaForm):
    """ Form handling for new LC

    This form can be accessed as @@add-new-lc.

    """

    grok.name('add-new-lc')
    grok.require('zope2.View')  # TODO: add permission
    grok.context(ISiteRoot)

    schema = INewLCForm
    ignoreContext = True

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # check if the Local Committees folder exists
        if not self.context.get('lc'):
            api.content.create(
                type='Folder',
                title='Local Committees',
                id='lc',
                container=self.context
            )

        # add a new LC object
        lc = api.content.create(
            type='eestec.portal.lc',
            title=self.request.form.get('form.widgets.city'),
            container=self.context.lc
        )

        # create a user for the CP
        user = api.user.create(
            username=self.request.form.get('form.widgets.cp_username'),
            email=self.request.form.get('form.widgets.cp_email'),
            properties=dict(
                fullname=self.request.form.get('form.widgets.cp_fullname'),
                )
        )

        # create LC members group
        members = api.group.create(
            groupname=lc.id,
        )

        # create LC Board group
        board = api.group.create(
            groupname="%s-board" % lc.id,
        )

        # join user to LC groups
        api.user.join_group(
            user=user,
            group=members,
        )
        api.user.join_group(
            user=user,
            group=board,
        )

        # TODO: proper body text
        api.portal.send_email(
            sender="admin@mysite.com",
            body="TODO: bla bla",
            recipient=user.getProperty('email'),
            subject="TODO: bla bla",
        )

        # Done!
        self.status = "LC added."

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""
        pass
