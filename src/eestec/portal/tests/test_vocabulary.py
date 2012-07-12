#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eestec.portal.tests.base import IntegrationTestCase
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestLCListVocabulary(IntegrationTestCase):
    """Test the vocabulary that renturns a list of LCs
    """

    def setUp(self):
        self.portal = self.layer['portal']

        api.content.create(
            type='eestec.portal.lc',
            title=u'patra',
            container=self.portal
        )

        api.content.create(
            type='eestec.portal.lc',
            title=u'athens',
            container=self.portal
        )
        factory = getUtility(IVocabularyFactory, 'lc_list')
        self.vocabulary = factory(self.portal)

    def test_returned_list(self):
        self.assertEquals([u'patra', u'athens'], [i.title for i in self.vocabulary])
