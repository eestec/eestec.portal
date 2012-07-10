from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EestecPortalUserDataPanelAdapter(UserDataPanelAdapter):
    """ """
    def get_lc(self):
        return self.context.getProperty('lc', '')
    def set_lc(self, value):
        return self.context.setMemberProperties({'lc': value})
    lc = property(get_lc, set_lc)

    # def get_mobile(self):
    #     return self.context.getProperty('mobile', '')
    # def set_mobile(self, value):
    #     return self.context.setMemberProperties({'mobile': value})
    # mobile = property(get_mobile, set_mobile)

    # def get_study_field(self):
    #     return self.context.getProperty('study_field', '')
    # def set_study_field(self, value):
    #     return self.context.setMemberProperties({'study_field': value})
    # study_field = property(get_study_field, set_study_field)

    # def get_birthdate(self):
    #     return self.context.getProperty('birthdate', '')
    # def set_birthdate(self, value):
    #     return self.context.setMemberProperties({'birthdate': value})
    # birthdate = property(get_birthdate, set_birthdate)

    # def get_sex(self):
    #     return self.context.getProperty('sex', '')
    # def set_sex(self, value):
    #     return self.context.setMemberProperties({'sex': value})
    # sex = property(get_sex, set_sex)

    # def get_nationality(self):
    #     return self.context.getProperty('nationality', '')
    # def set_nationality(self, value):
    #     return self.context.setMemberProperties({'nationality': value})
    # nationality = property(get_nationality, set_nationality)

    # def get_address(self):
    #     return self.context.getProperty('address', '')
    # def set_address(self, value):
    #     return self.context.setMemberProperties({'address': value})
    # address = property(get_address, set_address)

    # def get_passport_id(self):
    #     return self.context.getProperty('passport_id', '')
    # def set_passport_id(self, value):
    #     return self.context.setMemberProperties({'passport_id': value})
    # passport_id = property(get_passport_id, set_passport_id)

    # def get_passport_date_of_issue(self):
    #     return self.context.getProperty('passport_date_of_issue', '')
    # def set_passport_date_of_issue(self, value):
    #     return self.context.setMemberProperties({'passport_date_of_issue': value})
    # passport_date_of_issue = property(get_passport_date_of_issue, set_passport_date_of_issue)

    # def get_passport_valid_until(self):
    #     return self.context.getProperty('passport_valid_until', '')
    # def set_passport_valid_until(self, value):
    #     return self.context.setMemberProperties({'passport_valid_until': value})
    # passport_valid_until = property(get_passport_valid_until, set_passport_valid_until)

    # def get_tshirt_size(self):
    #     return self.context.getProperty('tshirt_size', '')
    # def set_tshirt_size(self, value):
    #     return self.context.setMemberProperties({'tshirt_size': value})
    # tshirt_size = property(get_tshirt_size, set_tshirt_size)

    # def get_needs(self):
    #     return self.context.getProperty('needs', '')
    # def set_needs(self, value):
    #     return self.context.setMemberProperties({'needs': value})
    # needs = property(get_needs, set_needs)

    # def get_captcha(self):
    #     return self.context.getProperty('captcha', '')
    # def set_captcha(self, value):
    #     return self.context.setMemberProperties({'captcha': value})
    # captcha = property(get_captcha, set_captcha)

    # def get_warning(self):
    #     return self.context.getProperty('warning', '')
    # def set_warning(self, value):
    #     return self.context.setMemberProperties({'warning': value})
    # warning = property(get_warning, set_warning)
