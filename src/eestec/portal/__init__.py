# -*- coding: utf-8 -*-
"""Init and utils."""

LC_MEMBERS_GROUP_STRING = u'%s-members'
LC_BOARD_GROUP_STRING = u'%s-board'

CP_LIST_ADDRESS = 'cp@eestec.net'
BOARD_LIST_ADDRESS = 'board@eestec.net'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


# Make the image of News Items a required field
from Products.ATContentTypes.atct import ATNewsItem
ATNewsItem.schema['image'].required = True
