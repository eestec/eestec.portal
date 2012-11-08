# -*- coding: utf-8 -*-
"""Testing our Vocabularies."""

from eestec.portal.tests.base import IntegrationTestCase
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestLCListVocabulary(IntegrationTestCase):
    """Test the vocabulary that renturns a list of LCs
    """

    def setUp(self):
        self.portal = self.layer['portal']

        # the vocabulary calls lc.full_title() which expects that LCs have
        # workflows enabled
        self.workflow = api.portal.get_tool('portal_workflow')
        self.workflow.setChainForPortalTypes(
            ['eestec.portal.lc'],
            'lc_workflow'
        )

        # creat the LCs folder
        api.content.create(
            type='Folder',
            title=u'Local Committees',
            id='lc',
            container=self.portal
        )

        # create a couple of LCs
        api.content.create(
            type='eestec.portal.lc',
            title=u'Niš',
            container=self.portal.lc
        )
        api.content.create(
            type='eestec.portal.lc',
            title=u'Novi Sad',
            container=self.portal.lc
        )

    def test_vocabulary(self):
        factory = getUtility(IVocabularyFactory, 'lc_list')
        self.vocabulary = factory(self.portal)

        self.assertEquals(
            [u'Observer Ni\u0161', u'Observer Novi Sad'],
            [i.title for i in self.vocabulary]
        )
