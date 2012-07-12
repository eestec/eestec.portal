#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plone import api

from eestec.portal.tests.base import IntegrationTestCase


class TestEventApplication(IntegrationTestCase):
    """Test eestec EventApplication type."""

    def setUp(self):
        self.portal = self.layer['portal']
        #self.workflow = api.get_tool('portal_workflow')

        # TODO: in tests we have to manually map content types to workflows
        #self.workflow.setDefaultChain('eventapplication_workflow')

        # create an LC
        self.lc = api.content.create(
            type='eestec.portal.lc',
            title=u'Niš',
            container=self.portal,
        )
        self.event = api.content.create(
            type='eestec.portal.event',
            title=u'Beer sprint',
            container=self.lc,
        )
        self.eventapp = api.content.create(
            type='eestec.portal.eventapplication',
            id='eapp',
            container=self.event,
        )

    def test_applicant_fullname_and_lc(self):
        pass

#    def test_get_lc_title(self):
#        raise NotImplemented
