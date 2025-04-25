from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings

from edc_randomization.auth_objects import RANDO_UNBLINDED
from edc_randomization.blinding import (
    raise_if_prohibited_from_unblinded_rando_group,
    trial_is_blinded,
    user_is_blinded,
)

from ..testcase_mixin import TestCaseMixin


class TestRandomizer(TestCaseMixin, TestCase):
    @override_settings(EDC_RANDOMIZATION_BLINDED_TRIAL=True)
    def test_trial_is_blinded(self):
        self.assertTrue(trial_is_blinded())

    @override_settings(EDC_RANDOMIZATION_BLINDED_TRIAL=False)
    def test_is_not_blinded_trial(self):
        self.assertFalse(trial_is_blinded())

    @override_settings(EDC_RANDOMIZATION_BLINDED_TRIAL=None)
    def test_is_blinded(self):
        self.assertTrue(trial_is_blinded())

    @override_settings(EDC_RANDOMIZATION_UNBLINDED_USERS=[])
    def test_user_is_blinded1(self):
        self.assertTrue(user_is_blinded("audrey"))

    @override_settings(EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"])
    def test_user_is_blinded2(self):
        self.assertTrue(user_is_blinded("audrey"))

    @override_settings(EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"])
    def test_user_is_blinded3(self):
        get_user_model().objects.create(username="audrey")
        self.assertTrue(user_is_blinded("audrey"))

    @override_settings(EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"])
    def test_is_unblinded_user(self):
        get_user_model().objects.create(username="audrey", is_staff=True, is_active=True)
        self.assertFalse(user_is_blinded("audrey"))

    @override_settings(
        EDC_RANDOMIZATION_BLINDED_TRIAL=False, EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"]
    )
    def test_listed_as_unblinded_user_but_trial_is_not_a_blinded_trial(self):
        get_user_model().objects.create(username="audrey", is_staff=True, is_active=True)
        self.assertFalse(user_is_blinded("audrey"))

    @override_settings(
        EDC_RANDOMIZATION_BLINDED_TRIAL=True, EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"]
    )
    def test_is_unblinded_user_in_a_blinded_trial(self):
        get_user_model().objects.create(username="audrey", is_staff=True, is_active=True)
        self.assertFalse(user_is_blinded("audrey"))

    @override_settings(
        EDC_RANDOMIZATION_BLINDED_TRIAL=True, EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"]
    )
    def test_form_validator_for_auth(self):
        user = get_user_model().objects.create(
            username="audrey", is_staff=True, is_active=True
        )
        grp = Group.objects.create(name=RANDO_UNBLINDED)
        user.groups.add(grp)
        grps = user.groups.all()

        try:
            raise_if_prohibited_from_unblinded_rando_group(user.username, grps)
        except forms.ValidationError:
            self.fail("forms.ValidationError unexpectedly raised")

    @override_settings(
        EDC_RANDOMIZATION_BLINDED_TRIAL=True, EDC_RANDOMIZATION_UNBLINDED_USERS=["audrey"]
    )
    def test_form_validator_for_auth2(self):
        user = get_user_model().objects.create(
            username="tebogo", is_staff=True, is_active=True
        )
        grp = Group.objects.create(name=RANDO_UNBLINDED)
        user.groups.add(grp)
        grps = user.groups.all()

        self.assertRaises(
            forms.ValidationError,
            raise_if_prohibited_from_unblinded_rando_group,
            user.username,
            grps,
        )
