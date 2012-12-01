# -*- coding: utf-8 -*-
"""The LC content type."""

from eestec.portal import LC_BOARD_GROUP_STRING
from eestec.portal import LC_MEMBERS_GROUP_STRING
from eestec.portal import emails
from five import grok
from plone import api
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.CMFCore.interfaces import ISiteRoot
from z3c.form import button
from zope import schema


class ILC(form.Schema, IImageScaleTraversable):
    """LC field specification."""

    # read http://davidjb.com/blog/2010/04/plone-and-dexterity-working-with-computed-fields
    # and see if this title->city relation can be done better

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

    # TODO: add validation to these fields to check if LC/member already exists
    city = schema.TextLine(
        title=u"City",
        description=u"City name of a LC",
    )

    # CP == Contact Person
    cp_fullname = schema.TextLine(
        title=u"CP full name",
        description=u"Contact person full name",
    )

    cp_username = schema.TextLine(
        title=u"CP username",
        description=u"Contact person username",
    )

    cp_email = schema.TextLine(
        title=u"CP email",
        description=u"Contact person email",
    )


class AddLCForm(form.SchemaForm):
    """Form for adding a new LC.

    When adding a new LC we cannot use the default Plone 'add new ...' form,
    because we need additional information (like CP name and email) and special
    handling. Hence a custom form for adding a new LC.
    """

    grok.name('add-lc')
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

        self.create()

        # Done!
        self.status = 'LC added.'

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""
        pass

    def create(self):
        """Add a new LC, it's CP and groups; plus assign roles/permissions."""

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
            groupname=LC_MEMBERS_GROUP_STRING % lc.id,
        )

        # create LC Board group
        board = api.group.create(
            groupname=LC_BOARD_GROUP_STRING % lc.id,
        )

        # join user to LC groups
        api.group.add_user(
            group=members,
            user=user,
        )
        api.group.add_user(
            user=user,
            group=board,
        )

        # give the LC Board their permissions over LC
        lc.manage_setLocalRoles(
            board.id,
            ['LCBoard', 'Contributor', 'Reviewer', 'Reader'])

        # give the LC Board permission to add new members to their LC
        api.group.grant_roles(
            group=board,
            roles=['MemberAdder', ],
        )

        # user in this context refers to newly-created CP of new LC
        emails.lc.lc_created_notify_cp(lc, user)
