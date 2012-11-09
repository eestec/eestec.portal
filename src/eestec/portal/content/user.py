# -*- coding: utf-8 -*-
"""User object. We use the default Plone user objects of the MemberData class
and just extend/override some stuff with eestec.portal specifics.
"""

from datetime import date
from eestec.portal.const import COUNTRIES
from eestec.portal.const import SEXES
from eestec.portal.const import STUDY_FIELDS
from eestec.portal.const import TSHIRT_SIZES
from plone import api
from plone.app.users.browser.personalpreferences import UserDataConfiglet
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class LCVocabulary(object):
    """Will return a list of all LCs."""

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []

        lc_folder = api.portal.get().lc
        for lc_id, lc in lc_folder.items():

            # only add LC types as vocabulary terms
            if not lc.portal_type == 'eestec.portal.lc':
                continue

            terms.append(
                SimpleTerm(
                    value=unicode(lc_id),
                    token=unicode(lc_id),
                    title=lc.full_title(),
                )
            )

        return SimpleVocabulary(terms)


LCVocabularyFactory = LCVocabulary()


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
        required=True,
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
        required=True,
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
        required=True,
    )

    passport_id = schema.TextLine(
        title=u'Passport ID',
        description=u"Passport Details",
        required=True,
    )

    passport_date_of_issue = schema.Date(
        title=u'Passport date of issue',
        description=u"Passport Details",
        min=date.today().replace(year=date.today().year - 10),
        max=date.today(),
    )

    passport_valid_until = schema.Date(
        title=u'Passport valid until',
        description=u"Passport Details",
        max=date.today().replace(year=date.today().year + 10),
        min=date.today(),
    )

    tshirt_size = schema.Choice(
        title=u'T-Shirt size',
        constraint=Validate.sizes,
        description=u"Select your T-Shirt size.",
        values=TSHIRT_SIZES,
    )

    needs = schema.Text(
        title=u'Special needs',
        description=u"Any special needs? Food allergies? Medical \
        issues? Anything the organizers need to be \
        aware of? Anything the organizers need to \
        tell us?",
    )


class EestecPortalUserDataPanelAdapter(UserDataPanelAdapter):
    """Adapt Plone's user object with our specific getters/setters."""

    def get_lc(self):
        return self.context.getProperty('lc', '')

    def set_lc(self, value):
        return self.context.setMemberProperties({'lc': value})
    lc = property(get_lc, set_lc)

    def get_mobile(self):
        return self.context.getProperty('mobile', '')

    def set_mobile(self, value):
        return self.context.setMemberProperties({'mobile': value})
    mobile = property(get_mobile, set_mobile)

    def get_study_field(self):
        return self.context.getProperty('study_field', '')

    def set_study_field(self, value):
        return self.context.setMemberProperties({'study_field': value})
    study_field = property(get_study_field, set_study_field)

    def get_birthdate(self):
        return self.context.getProperty('birthdate', '')

    def set_birthdate(self, value):
        return self.context.setMemberProperties({'birthdate': value})
    birthdate = property(get_birthdate, set_birthdate)

    def get_sex(self):
        return self.context.getProperty('sex', '')

    def set_sex(self, value):
        return self.context.setMemberProperties({'sex': value})
    sex = property(get_sex, set_sex)

    def get_nationality(self):
        return self.context.getProperty('nationality', '')

    def set_nationality(self, value):
        return self.context.setMemberProperties({'nationality': value})
    nationality = property(get_nationality, set_nationality)

    def get_address(self):
        return self.context.getProperty('address', '')

    def set_address(self, value):
        return self.context.setMemberProperties({'address': value})
    address = property(get_address, set_address)

    def get_passport_id(self):
        return self.context.getProperty('passport_id', '')

    def set_passport_id(self, value):
        return self.context.setMemberProperties({'passport_id': value})
    passport_id = property(get_passport_id, set_passport_id)

    def get_passport_date_of_issue(self):
        return self.context.getProperty('passport_date_of_issue', '')

    def set_passport_date_of_issue(self, value):
        return self.context.setMemberProperties(
            {'passport_date_of_issue': value})
    passport_date_of_issue = property(
        get_passport_date_of_issue,
        set_passport_date_of_issue
    )

    def get_passport_valid_until(self):
        return self.context.getProperty('passport_valid_until', '')

    def set_passport_valid_until(self, value):
        return self.context.setMemberProperties(
            {'passport_valid_until': value})
    passport_valid_until = property(
        get_passport_valid_until,
        set_passport_valid_until
    )

    def get_tshirt_size(self):
        return self.context.getProperty('tshirt_size', '')

    def set_tshirt_size(self, value):
        return self.context.setMemberProperties({'tshirt_size': value})
    tshirt_size = property(get_tshirt_size, set_tshirt_size)

    def get_needs(self):
        return self.context.getProperty('needs', '')

    def set_needs(self, value):
        return self.context.setMemberProperties({'needs': value})
    needs = property(get_needs, set_needs)

    def get_captcha(self):
        return self.context.getProperty('captcha', '')

    def set_captcha(self, value):
        return self.context.setMemberProperties({'captcha': value})
    captcha = property(get_captcha, set_captcha)

    def get_warning(self):
        return self.context.getProperty('warning', '')

    def set_warning(self, value):
        return self.context.setMemberProperties({'warning': value})
    warning = property(get_warning, set_warning)


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """Override the IUserDataSchemaProvider to return our custom schema."""
        return IEestecPortalUserDataSchema


class EestecPortalUserDataConfiglet(UserDataConfiglet):
    """Customize @@user-information view."""

    def __call__(self):
        # Omit default Plone fields
        self.form_fields = self.form_fields.omit(
            'home_page',
            'description',
            'location',
            'pdelete',
        )

        return super(EestecPortalUserDataConfiglet, self).__call__()


class PLRUserDataPanel(UserDataPanel):
    """Customize @@personal-information view."""

    def __call__(self):
        # Omit Plone default fields
        self.form_fields = self.form_fields.omit(
            'home_page',
            'description',
            'location',
            'pdelete',
        )

        return super(PLRUserDataPanel, self).__call__()
