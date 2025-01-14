"""
Tests for managing the (admin) user preferences.
"""
from django.urls import reverse, reverse_lazy

from django_webtest import WebTest
from furl import furl

from .factories import StaffUserFactory, SuperUserFactory, UserFactory


class AccessControlTests(WebTest):
    admin_url = reverse_lazy("admin:accounts_userpreferences_change")

    def test_anonymous_user(self):
        response = self.app.get(self.admin_url)

        expected_redirect = furl(reverse("admin:login")).set(
            {"next": str(self.admin_url)}
        )
        self.assertRedirects(response, str(expected_redirect))

    def test_non_staff_user(self):
        user = UserFactory.create(is_staff=False, is_superuser=False)

        response = self.app.get(self.admin_url, user=user)

        expected_redirect = furl(reverse("admin:login")).set(
            {"next": str(self.admin_url)}
        )
        self.assertRedirects(response, str(expected_redirect))

    def test_superuser_but_not_staff(self):
        user = SuperUserFactory.create(is_staff=False)

        response = self.app.get(self.admin_url, user=user)

        expected_redirect = furl(reverse("admin:login")).set(
            {"next": str(self.admin_url)}
        )
        self.assertRedirects(response, str(expected_redirect))

    def test_staff_users(self):
        for is_superuser in (False, True):
            with self.subTest(is_superuser=is_superuser):
                user = StaffUserFactory.create(is_superuser=is_superuser)

                response = self.app.get(self.admin_url, user=user)

                self.assertEqual(response.status_code, 200)

    def test_fiddling_with_urls(self):
        staff_user = StaffUserFactory.create()
        other_user = StaffUserFactory.create()
        url = reverse(
            "admin:accounts_userpreferences_change",
            kwargs={"object_id": str(other_user.pk)},
        )

        response = self.app.get(url, user=staff_user, status=403)

        self.assertEqual(response.status_code, 403)


class UserPreferencesTests(WebTest):
    admin_url = reverse_lazy("admin:accounts_userpreferences_change")

    def test_prevent_accidentally_exposed_fields(self):
        staff_user = StaffUserFactory.create()
        non_model_fields = {"csrfmiddlewaretoken", "_save"}

        change_page = self.app.get(self.admin_url, user=staff_user)

        form_fields = set(change_page.form.fields.keys())
        self.assertEqual(form_fields, {"ui_language"} | non_model_fields)

    def test_can_update_language_preference(self):
        staff_user = StaffUserFactory.create(ui_language="")
        change_page = self.app.get(self.admin_url, user=staff_user)

        change_page.form["ui_language"].select("en")
        change_page.form.submit(name="_save")

        staff_user.refresh_from_db()
        self.assertEqual(staff_user.ui_language, "en")
