from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITest(APITestCase):
    def setUp(self):
        Education.objects.all().delete()
        self.owner = User.objects.create_superuser("edu_owner", "owner@example.com", "test-password")
        self.visitor = User.objects.create_user("edu_visitor", password="test-password")
        self.editor = User.objects.create_user("edu_editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.payload = {"institution": "Sekolah Contoh", "program": "IPA", "start_year": 2022, "end_year": 2025}
        self.education = Education.objects.create(**self.payload)
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])

    def assert_unchanged(self):
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        for field, value in self.payload.items():
            self.assertEqual(getattr(self.education, field), value)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_public_read_search_and_missing(self):
        for user in (None, self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.get(self.list_url, {"institution": "SEKOLAH"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], self.education.pk)
            self.assertFalse(response.data[0]["is_starred"])
            self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(self.list_url, {"institution": "missing"}).data, [])
        self.assertEqual(self.client.get(reverse("api:education-detail", args=[self.education.pk + 1000])).status_code, 404)

    def test_guest_and_regular_user_cannot_manage_data(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url, payload in [
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, {**self.payload, "program": "Changed"}),
                ("patch", self.detail_url, {"program": "Changed"}),
                ("delete", self.detail_url, {}),
            ]:
                with self.subTest(user=user, method=method):
                    self.assertEqual(getattr(self.client, method)(url, payload, format="json").status_code, 403)
                    self.assert_unchanged()

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assert_unchanged()
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assert_unchanged()
        self.assertEqual(self.client.patch(self.detail_url, {"program": "Sistem Informasi"}, format="json").status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.program, "Sistem Informasi")
        self.assertEqual(self.education.institution, self.payload["institution"])
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assert_unchanged()

    def test_owner_create_update_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {**self.payload, "end_year": None}, format="json")
        self.assertEqual(response.status_code, 201)
        pk = response.data["id"]
        self.assertIsNone(Education.objects.get(pk=pk).end_year)
        url = reverse("api:education-detail", args=[pk])
        self.assertEqual(self.client.patch(url, {"program": "Musik"}, format="json").status_code, 200)
        self.assertEqual(Education.objects.get(pk=pk).program, "Musik")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=pk).exists())

    def test_validation_and_cleaning(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution": "   "}, "institution"),
            ({"institution": '<img src=x onerror="alert(1)">'}, "institution"),
            ({"program": "<b></b>"}, "program"),
            ({"start_year": -1}, "start_year"),
            ({"end_year": 2021}, "end_year"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
            self.assert_unchanged()
        response = self.client.post(self.list_url, {**self.payload, "institution": "<b>Sekolah</b>"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.get(pk=response.data["id"]).institution, "Sekolah")

    def test_partial_year_validation_and_full_update_required_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"start_year": 2026}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("end_year", response.data)
        self.assertEqual(self.client.put(self.detail_url, {"program": "IPA"}, format="json").status_code, 400)
        self.assert_unchanged()

    def test_star_uses_current_user_and_requires_login(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assert_unchanged()
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.data["is_starred"])
            self.assertEqual(response.data["star_count"], 1)
            self.assertEqual(list(self.education.starred_by.all()), [user])
            response = self.client.post(self.star_url)
            self.assertFalse(response.data["is_starred"])
            self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_cannot_be_forged_and_no_private_fields(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": 999999, "star_count": 100, "is_starred": True,
            "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 999999)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(set(response.data), {"id", "institution", "program", "start_year", "end_year", "star_count", "is_starred"})

    def test_session_csrf_required_and_valid_token_accepted(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="edu_owner", password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assert_unchanged()
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, 200)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)

    def test_wrong_methods(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assert_unchanged()

    def test_education_page_exposes_drf_routes_and_role_controls(self):
        for user in (None, self.visitor, self.editor, self.owner):
            self.client.logout()
            if user:
                self.client.force_login(user)
            response = self.client.get(reverse("main:show_education"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'data-api-url="/api/v1/education/"')
            self.assertContains(response, 'data-detail-url="/api/v1/education/0/"')
            self.assertContains(response, 'data-star-url="/api/v1/education/0/star/"')
            self.assertContains(response, 'name="csrfmiddlewaretoken"')
            if user in (self.editor, self.owner):
                self.assertContains(response, 'id="education-modal"')
                self.assertContains(response, 'action="/api/v1/education/"')
            else:
                self.assertNotContains(response, 'id="education-modal"')
            if user == self.owner:
                self.assertContains(response, '+ Tambah Pendidikan')
            else:
                self.assertNotContains(response, '+ Tambah Pendidikan')
