#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Products.CMFCore.interfaces import ISiteRoot
from five import grok
from plone import api
from plone.api import content
from plone.api import user
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form import button, validator
from z3c.schema.email import RFC822MailAddress
from zope import schema
import zope.component


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

    # XXX we copied the grok lines from a skeleton
    grok.name('add-new-lc')
    grok.require('zope2.View')
    grok.context(ISiteRoot)

    schema = INewLCForm
    ignoreContext = True

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if not self.context.get('lc'):
            content.create(
                type='Folder',
                title='Local Committees',
                container=self.context
            )


        # Do something with valid data here

        #content.create(
            #type='eestec.portal.lc',
            #title=self.request.get('city'),
            #container=self.context.lc
        #)
        import pdb; pdb.set_trace()

        try:
            user.create(
                username=self.request.form.get('form.widgets.cp_username'),
                email=self.request.form.get('form.widgets.cp_email'),
                roles=(),
                properties=dict(
                    fullname=self.request.form.get('form.widgets.cp_fullname'),
                    )
            )
        except Exception, e:
            api.show_message("Can not add a RC: %s" % e)




        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "Thank you very much!"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""
