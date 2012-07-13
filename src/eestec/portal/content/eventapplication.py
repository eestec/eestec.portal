# -*- coding: utf-8 -*-
"""The event application content type."""

from eestec.portal import emails
from five import grok
from plone import api
from plone.app.textfield import RichText
from plone.directives import form, dexterity
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface.declarations import alsoProvides


class IEventApplication(form.Schema):
    """Application that eestecers will submit to apply to an LC event.
    """

    # TODO: this doesn't work. instructions should haven no input
    form.mode(IEditForm, instructions='display')
    instructions = schema.TextLine(
        title=u"All personal information that the organizers need will be pulled from your profile.",
        description=u'Please make sure that you have filled in all personal information in your profile page.',
        required=False,
    )

    notes = RichText(
        title=u'Additional notes / Motivational letter',
        description=u'Any additional notes/information you would like to give to the organizers, besides the information that is already in your profile page?',
    )

    arrival = schema.Datetime(
        title=u'Arrival Date/Time',
        description=u'Please input your arrival date/time.',
    )

    departure = schema.Datetime(
        title=u'Departure Date/Time',
        description=u'Please input your departure date/time.',
    )

    arrival_notes = schema.Text(
        title=u'Arrival notes / Type of transport',
        description=u'Any additional information about your arrival. Type of transportation, flight information, etc',
    )

    departure_notes = schema.Text(
        title=u'Departure notes / Type of transport',
        description=u'any additional information about your departure. type of transportation, flight information, etc',
    )

alsoProvides(IEventApplication, form.IFormFieldProvider)


class EventApplication(dexterity.Container):
    """
    """
    grok.implements(IEventApplication)

    def get_applicant_fullname_and_lc(self):
        """Return member's fullname along with it's LC."""
        user = api.user.get(username=self.Creator())
        return u"%s, %s" % (user.fullname, self.get_lc_title())

    @property
    def Title(self):
        return self.get_fullname_with_lc()

    def get_lc_title(self):
        """Return's full-title of LC."""
        portal = api.portal.get()
        user = api.user.get(username=self.Creator())
        lc = portal.lc.get(user.lc)
        return lc.full_title()

    @property
    def lc(self):
        return self.get_lc_title()


# TODO: write subscribers for eventapplication
def eventapplication_created(context, event):
    """
    #. Send email to member's LC Board.
    #. Send email to organizer's LC Board.
    #. Send email to member.
    """

    emails.event_application_lc_board_notification(context)
    emails.event_application_organizers_notification(context)
    emails.event_application_member_notification(context)


def eventapplication_workflow_transitioned(context, event):
    """
    #. Send accepted notification email to member
    #. Send accepted notification email to member's LC Board.
    #. Send rejected notification email to member
    #. Send reject notification email to member's LC Board.
    """

    if event.transition and event.transition.id == "accept_participant":
        emails.event_application_accepted_member_notification(context)
        emails.event_application_accepted_lc_board_notification(context)

    if event.transition and event.transition.id == "reject_participant":
        emails.event_application_rejected_member_notification(context)
        emails.event_application_rejected_lc_board_notification(context)
