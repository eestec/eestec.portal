from datetime import date

from zope.interface import Interface, implements
from zope import schema

# from collective.examples.userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

STUDY_FIELDS = ['ece', 'electrical engineering', 'engineering of electics', 'electrical']
SEXES = ['male', 'female']
COUNTRIES = ['greece' , 'USA', 'other countries']
TSHIRT_SIZES = ['Large', 'Medium', 'Gay']

class MemberValidator(object):
    """Information about an EESTEC member."""
    def __init__(self, study_fields, countries, tshirt_sizes, sexes):
        self.study_fields = study_fields
        self.countries = countries
        self.tshirt_sizes = tshirt_sizes
        self.sexes = sexes

    def LCs(self, val):
        """Return all registered LCs on the webpage."""
        portal_catalog = getToolByName(self, 'portal_catalog')

        brains = portal_catalog(Type='LC', sort_on='sortable_title')

        lcs = []
        for brain in brains:
            lcs.append((brain.getObject().getId(),
                        brain.getObject().getFull_lc_title()))
        return val in lcs

    def current_LC(self, val):
        """Returns an object of the LC this EestecMember is a member of."""
        catalog = getToolByName(self, 'portal_catalog')
        return val in catalog(Type='LC', id=self.lc)[0].getObject()

    def study_fields(self, val):
        """Return all study fields that are specified in config.py."""
        return val in self.study_fields

    def sex(self):
        """Return options for the 'sex' drop-down menu."""
        return val in self.sexes

    def country(self, val):
        """Return all countries that are specified in config.py."""
        return val in self.countries

    def sizes(self, val):
        """Return all tshirt sizes that are specified in config.py."""
        return self.tshirt_sizes


### FIXME: The current date around wich dates are set is the day that
### the server started, not tha day of submission
class IEestecPortalUserDataSchema(IUserDataSchema):
    """Use all the fields from the default user data schema, and add
    various extra fields.
    """
    # _validator = MemberValidator(STUDY_FIELDS, COUNTRIES, TSHIRT_SIZES, SEXES)
    lc = schema.TextLine(
        title = u"LC",
        #validate = _validator.LCs,
        required=True,
        description=u"Select the Local Committee you belong to. If you \
        don't know what this is just leave it at \
        'Observer Candidates'."
        )

#     mobile = schema.TextLine(
#         title = _( u'mobile', default = u"Mobile"),
#         description="Enter the mobile number on which you are \
#         available for the organizers.",
#         # read_permission=ModifyPortalContent,
#         )

#     study_field = schema.TextLine(
#         title = _( u'study_field', default = u"Study Field"),
#         #validate=_validator.study_fields,
#         description="Select your study field.",
#         format='select',
#         )

#     birthdate = schema.Date(
#         title = _( u'birthdate', default = u"Birthdate"),
#         description="Select your birthdate.",
#         max = date.today(),
#         min = date(1964, 1, 1),
#         # read_permission=ModifyPortalContent,
#         )

#     sex = schema.Choice(
#         title = _( u'sex', default = u"Sex"),
#         validate=_validator.sex,
#         description="Select your sex.",
#         )

#     nationality = schema.Choice(
#         title = _( u'nationality', default = u"Nationality"),
#         validate=_validator.countries,
#         description="Passport Details",
#         values = NA
#         )

#     address = schema.TextLine(
#         title = _( u'address', default = u"Address"),
#         description="Passport Details",
#         # read_permission=ModifyPortalContent,
#         )

#     passport_id = schema.TextLine(
#         title = _( u'passport_id', default = u"Passport ID Number"),
#         description="Passport Details",
#         # read_permission=ModifyPortalContent,
#         )

#     passport_date_of_issue = schema.Date(
#         title = _( u'passport_date_of_issue', default = u"Date Of Issue"),
#         description="Passport Details",
#         min = date.today().replace(year=date.today().year - 10),
#         max = date.today(),
#         # read_permission=ModifyPortalContent,
#         )

#     passport_valid_until = schema.Date(
#         title = _( u'passport_valid_until', default = u"Valid Until"),
#         description="Passport Details",
#         max = date.today().replace(year=date.today().year + 10),
#         min = date.today(),
#         # read_permission=ModifyPortalContent,
#         )

#     tshirt_size = schema.Choice(
#         title = _( u'tshirt_size', default = u"T-Shirt size"),
#         validate=_validator.sizes,
#         description="Select your T-Shirt size.",
#         values = TSHIRT_SIZES,
#         # read_permission=ModifyPortalContent,
#         )

#     needs = schema.TextField(
#         title = _( u'needs', default = u"Special needs"),
#         description="Any special needs? Food allergies? Medical \
#         issues? Anything the organizers need to be \
#         aware of? Anything the organizers need to \
#         tell us?",
#         # read_permission=ModifyPortalContent,
#         )

#     captcha = schema.Int(
#         title = _( u'captcha', default = ustr(n1) + " + " + str(n2) + " is: "),
#         description="Captcha",
#         # read_permission=ModifyPortalContent,
#         required=True,
#         validator=_validator.range
#         )

#     warning = schema.TextLine(
#         title = _( u'warning', default = u"Warning!"),
#         description="In case you are applying for an Event \
#         for the first time, the system redirected you \
#         to this page (your profile page) so you enter \
#         all necessary information. Once you click 'save' \
#         your personal information will be saved. Then you \
#         need to GO BACK TO THE EVENT PAGE AND CLICK APPLY \
#         AGAIN!"
# )


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEestecPortalUserDataSchema
