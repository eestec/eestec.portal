#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plone.api import content
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema


class ILC(form.Schema, IImageScaleTraversable):
    """EESTEC Local Committee."""

    title = schema.TextLine(
        title=u"City",
        description=u"City name of the LC",
    )


class LC(dexterity.Container):
    grok.implements(ILC)

    def full_lc_title(self):
        """Return full name of LC, for example: JLC Antwerp."""
        if not self.id:
            return ''

        state = content.get_state(self)
        if state == 'inactive':
            state = '(inactive)'
        if state.lower() == 'observer':
            state = state.title()
        else:
            state = state.upper()
        return u'%s %s' % (state, self.title)
