#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plone import api
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
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

    @property
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
