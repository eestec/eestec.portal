# -*- coding: utf-8 -*-
"""Testing Users."""

from datetime import date
from eestec.portal.tests.base import FunctionalTestCase
from eestec.portal.tests.base import IntegrationTestCase
from plone import api
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

import unittest2 as unittest


class TestUserIntegration(IntegrationTestCase):
    """Testing user registration and fields."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_adapter_registration(self):
        """Test that self.portal is adapted by IEestecPortalUserDataSchema."""
        from eestec.portal.content.user import IEestecPortalUserDataSchema
        adapter = IEestecPortalUserDataSchema(self.portal)
        self.assertNotEquals(adapter, None)

    def test_fields_set_upon_user_creation(self):
        """Test that fields are correctly set when a user is created."""
        self.user = api.user.create(
            email='lois@plone.org',
            username='lois',
            properties=dict(
                lc=u'Quahog',
                mobile=u'666',
                study_field=u'housewife',
                birthdate=date(1960, 7, 22),
                sex=u'Female',
                nationality=u'USA',
                address=u'Rhode Island',
                passport_id=u'666',
                passport_date_of_issue=date.today(),
                passport_valid_until=date.today(),
                tshirt_size=u'Large',
                needs=u'No needs'
            )
        )

        self.assertEquals(self.user.getProperty('lc'), u'Quahog')
        self.assertEquals(self.user.getProperty('mobile'), u'666')
        self.assertEquals(self.user.getProperty('study_field'), u'housewife')
        self.assertEquals(self.user.getProperty('birthdate'), date(1960, 7, 22))
        self.assertEquals(self.user.getProperty('sex'), u'Female')
        self.assertEquals(self.user.getProperty('nationality'), u'USA')
        self.assertEquals(self.user.getProperty('address'), u'Rhode Island')
        self.assertEquals(self.user.getProperty('passport_id'), u'666')
        self.assertEquals(self.user.getProperty('tshirt_size'), u'Large')
        self.assertEquals(self.user.getProperty('needs'), u'No needs')
        self.assertEquals(
            self.user.getProperty('passport_date_of_issue'),
            date.today()
        )
        self.assertEquals(
            self.user.getProperty('passport_valid_until'),
            date.today()
        )


class TestUserFunctional(FunctionalTestCase):
    """Testing user registration and fields."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.browser = Browser(self.portal)

        # prepare request values for the new LC
        self.request.form['form.widgets.city'] = u'Niš'
        self.request.form['form.widgets.cp_username'] = 'jsmith'
        self.request.form['form.widgets.cp_fullname'] = u'Jöhn Smith'
        self.request.form['form.widgets.cp_email'] = 'john@eestec.net'

        # call the @@add-lc form to create us a new LC
        self.layer['portal'].restrictedTraverse('@@add-lc').create()

        # set CPs password
        cp = api.user.get(username='jsmith')
        self.portal.acl_users._doChangeUser(
            cp.id,
            TEST_USER_PASSWORD,
            cp.getRoles()
        )
        ### ARGH!!!! I hope the line above can be written with plone.api soon!

        # commit what we've done so testbrowser sees it
        import transaction
        transaction.commit()

    @unittest.expectedFailure
    def test_add_new_cp_member(self):
        """Test the LC Board can add a new member to their LC."""

        # Login as LC Boardie to add a new member
        self.login(username='jsmith')

        # Go to form to add new member
        self.browser.open('http://nohost/plone/@@register')
        open('/tmp/testbrowser.html', 'w').write(self.browser.contents)

        # Fill out the form
        self.browser.getControl(name='form.username').value = 'jane'
        self.browser.getControl(name='form.email').value = 'jane@eestec.net'
        self.browser.getControl(name='form.mobile').value = '+386 666'
        self.browser.getControl(name='form.study_field').value = ['ece', ]
        self.browser.getControl(name='form.birthdate').value = '1985/01/01'
        self.browser.getControl(name='form.sex').value = ['female', ]
        self.browser.getControl(name='form.nationality').value = ['greece', ]
        self.browser.getControl(name='form.tshirt_size').value = ['Medium', ]

        # Submit!
        self.browser.getControl(name='form.actions.register').click()

        # TODO: test that member was created!
