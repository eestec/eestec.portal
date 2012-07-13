#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Template controller for LC
--------------------------
"""

from eestec.portal.content import lc
from eestec.portal.content.lc import ILC

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from five import grok
from plone import  api


grok.templatedir('templates')

class ListLCMembers(grok.View):
    """
    View for displaying list of LC's members

    This renders a table displaying basic data of all the members in a LC.

    """
    grok.context(ILC)
    grok.require('zope2.View')
    grok.name('members-list')

    #def update(self):

        # Get the group maching the LC ID
        #
        #

    def members(self):
        """doc"""
        results = []

        self.context = aq_inner(self.context)
        self.lc_id = self.context.getId()

        self.group = api.group.get(groupname=self.lc_id)
        for member in self.group.getGroupMembers():
            results.append(dict(
                username=member.id,
                email=member.getProperty("email", "")
            ))

        return results
