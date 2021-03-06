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
from z3c.form import button
from zope import schema


class ILC(form.Schema, IImageScaleTraversable):
    """LC field specification."""

    # read http://davidjb.com/blog/2010/04/
    # /plone-and-dexterity-working-with-computed-fields
    # and see if this title->city relation can be done better

    # TODO: add validation to these fields to check if LC/member already exists
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


class IAddLCForm(form.Schema):
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


class AddForm(dexterity.AddForm):
    """Form for adding a new LC.

    When adding a new LC we cannot use the default Plone 'add new ...' form,
    because we need additional information (like CP name and email) and special
    handling. Hence a custom form for adding a new LC.
    """

    grok.name('eestec.portal.lc')
    schema = IAddLCForm

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.create()

        # Done, notify user and redirect back to LC folder
        api.portal.show_message(
            message="Successfully added LC {}.".format(data['city']),
            request=self.request,
        )
        self.request.RESPONSE.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page."""
        pass

    def create(self):
        """Add a new LC, its CP and groups; plus assign roles/permissions."""

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
                lc=self.request.form.get('form.widgets.city'),
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
            user=user,
            group=members,
        )
        api.group.add_user(
            user=user,
            group=board,
        )

        # allow LC Members to add content to their LC
        api.group.grant_roles(
            group=members,
            roles=['Contributor', ],
            obj=lc,
        )

        # allow LC Boardies to manage content in their LC
        api.group.grant_roles(
            group=board,
            roles=['Contributor', 'Reviewer', 'Reader'],
            obj=lc,
        )

        # allow LC Boardies to add new members to the site
        # NOTE: this role needs to be global!
        api.group.grant_roles(
            group=board,
            roles=['MemberAdder', ],
        )

        # send email to CP of newly created LC
        emails.lc.lc_created_notify_cp(lc, user)
        return lc
