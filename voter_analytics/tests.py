from datetime import date
from types import SimpleNamespace

from django.test import SimpleTestCase

from voter_analytics.templatetags.privacy import mask_dob, mask_name, mask_street


class PrivacyFilterTests(SimpleTestCase):
    def test_mask_name_hides_all_but_first_letter(self):
        self.assertEqual(mask_name("Jane"), "J***")
        self.assertEqual(mask_name("Al"), "A***")

    def test_mask_name_keeps_names_already_starred(self):
        self.assertEqual(mask_name("**F**"), "**F**")

    def test_mask_street_hides_number_and_apartment(self):
        voter = SimpleNamespace(street_number="17", street_name="CIRCUIT AVE", apartment_number="3")
        self.assertEqual(mask_street(voter), "*** CIRCUIT AVE")

    def test_mask_dob_shows_year_only(self):
        self.assertEqual(mask_dob(date(1980, 1, 3)), "**/**/1980")
