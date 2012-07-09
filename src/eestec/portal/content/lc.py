#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eestec.portal import _

from five import grok
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.CMFPlone.utils import getToolByName
from zope import schema


class ILC(form.Schema, IImageScaleTraversable):
    """Information about EESTEC Local Committee"""

    title = schema.TextLine(
        title=_(u"City"),
        description=_(u"City name of a LC"),
    )

    description = schema.Text(
        title=_(u"A short summary"),
    )


class LC(dexterity.Container):
    grok.implements(ILC)

    @property
    def full_lc_title(self):
        """Return full name of LC. Example: LC YesPlease"""
        if not self.id:
            return ''
        wf = getToolByName(self, 'portal_workflow')
        state = wf.getInfoFor(self, 'review_state').split(' ', 1)[0]
        if state == 'inactive':
            state = '(inactive)'
        if state.lower() == 'observer':
            state = state.title()
        else:
            state = state.upper()
        return u'%s %s' % (state, unicode(self.title, 'utf-8'))
