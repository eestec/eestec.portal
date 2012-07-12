# -*- coding: utf-8 -*-

from datetime import date

from zope.interface import implements
from zope import schema

# from collective.examples.userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


STUDY_FIELDS = ['ece', 'electrical engineering', 'engineering of electics', 'electrical']
SEXES = ['male', 'female']
COUNTRIES = ['greece', 'USA', 'other countries']
TSHIRT_SIZES = ['Large', 'Medium', 'Small']


class PortalTypesVocabulary(object):
    """Will return a list of all LCs"""

    implements(IVocabularyFactory)

    def __init__(self, portal_type):
        self.portal_type = portal_type

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog', None)
        if catalog is None:
            return SimpleVocabulary([])

        brains = catalog(portal_type=self.portal_type)
        items = [(brain.UID, brain.Title) for brain in brains]
        # Most schema fields expect unicode values.
        terms = [SimpleTerm(value=unicode(pair[0]), token=unicode(pair[0]),
                             title=pair[1]) for pair in items]
        return SimpleVocabulary(terms)


# Pick the portal_type that you want here:
PFGFormsVocabularyFactory = PortalTypesVocabulary('eestec.portal.lc')


class Validate:
    def study_fields(val):
        """Return all study fields that are specified in config.py."""
        return val in STUDY_FIELDS

    def sex(val):
        """Return options for the 'sex' drop-down menu."""
        return val in SEXES

    def country(val):
        """Return all countries that are specified in config.py."""
        return val in COUNTRIES

    def sizes(val):
        """Return all tshirt sizes that are specified in config.py."""
        return TSHIRT_SIZES


### FIXME: The current date around wich dates are set is the day that
### the server started, not tha day of submission
class IEestecPortalUserDataSchema(IUserDataSchema):
    """Use all the fields from the default user data schema, and add
    various extra fields."""

    lc = schema.Choice(
        title=u"LC",
        vocabulary="lc_list",
        required=True,
        description=u"Select the Local Committee you belong to. If you \
        don't know what this is just leave it at \
        'Observer Candidates'."
    )

    mobile = schema.TextLine(
        title=u'Mobile',
        description=u"Enter the mobile number on which you are \
        available for the organizers.",
        # read_permission = ModifyPortalContent,
    )

    study_field = schema.Choice(
        title=u'Study Field',
        constraint=Validate.study_fields,
        description=u"Select your study field.",
        values=STUDY_FIELDS,
    )

    birthdate = schema.Date(
        title=u'Birthdate',
        description=u"Select your birthdate.",
        max=date.today(),
        min=date(1964, 1, 1),
        # read_permission = ModifyPortalContent,
    )

    sex = schema.Choice(
        title=u'Sex',
        constraint=Validate.sex,
        description=u"Select your sex.",
        values=SEXES,
    )

    nationality = schema.Choice(
        title=u'Nationality',
        constraint=Validate.country,
        description=u"Passport Details",
        values=COUNTRIES
    )

    address = schema.TextLine(
        title=u'Address',
        description=u"Passport Details",
        # read_permission = ModifyPortalContent,
    )

    passport_id = schema.TextLine(
        title=u'Passport ID',
        description=u"Passport Details",
        # read_permission = ModifyPortalContent,
    )

    passport_date_of_issue = schema.Date(
        title=u'Passport date of issue',
        description=u"Passport Details",
        min=date.today().replace(year=date.today().year - 10),
        max=date.today(),
        # read_permission = ModifyPortalContent,
    )

    passport_valid_until = schema.Date(
        title=u'Passport valid until',
        description=u"Passport Details",
        max=date.today().replace(year=date.today().year + 10),
        min=date.today(),
        # read_permission = ModifyPortalContent,
    )

    tshirt_size = schema.Choice(
        title=u'T-Shirt size',
        constraint=Validate.sizes,
        description=u"Select your T-Shirt size.",
        values=TSHIRT_SIZES,
        # read_permission = ModifyPortalContent,
    )

    needs = schema.Text(
        title=u'Special needs',
        description=u"Any special needs? Food allergies? Medical \
        issues? Anything the organizers need to be \
        aware of? Anything the organizers need to \
        tell us?",
        # read_permission = ModifyPortalContent,
    )

    # FIXME: Add image and everything
    captcha = schema.Int(
        title=u'Captcha',
        description=u"Captcha",
        # read_permission = ModifyPortalContent,
        required=True,
    )

    # FIXME: displays an inputline
    warning = schema.TextLine(
        title=u'Warning',
        description=u"In case you are applying for an Event \
        for the first time, the system redirected you \
        to this page (your profile page) so you enter \
        all necessary information. Once you click 'save' \
        your personal information will be saved. Then you \
        need to GO BACK TO THE EVENT PAGE AND CLICK APPLY \
        AGAIN!"
    )


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEestecPortalUserDataSchema
