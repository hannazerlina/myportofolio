from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse


@override_settings(
    CORS_ALLOWED_ORIGINS=["http://127.0.0.1:8099"],
    CSRF_TRUSTED_ORIGINS=["http://127.0.0.1:8099"],
)
class MobileAuthTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.origin = "http://127.0.0.1:8099"
        self.password = "Local-example-password-482"
        self.session_url = reverse("mobile_auth:session")

    def post(self, name, data, token):
        return self.client.post(
            reverse(f"mobile_auth:{name}"), data, content_type="application/json",
            HTTP_X_CSRFTOKEN=token, HTTP_ORIGIN=self.origin,
        )

    def test_register_login_and_logout_with_csrf(self):
        data = {"username": "mobile-demo", "password": self.password}
        self.assertEqual(self.post("login", data, "").status_code, 403)
        session = self.client.get(self.session_url, HTTP_ORIGIN=self.origin)
        self.assertIsNone(session.json()["username"])
        self.assertEqual(session["Access-Control-Allow-Origin"], self.origin)
        token = session.json()["csrf_token"]

        self.assertEqual(self.post("login", data, token).status_code, 401)
        register = {"username": "mobile-demo", "password1": self.password, "password2": self.password}
        self.assertEqual(self.post("register", register, token).status_code, 201)
        self.assertEqual(self.post("register", register, token).status_code, 400)
        self.assertFalse(get_user_model().objects.get(username="mobile-demo").is_superuser)

        login = self.post("login", data, token)
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.json()["username"], "mobile-demo")
        self.assertFalse(login.json()["can_manage_projects"])
        self.assertEqual(self.client.get(self.session_url).json()["username"], "mobile-demo")
        self.assertEqual(self.post("logout", {}, token).status_code, 403)
        logout = self.post("logout", {}, login.json()["csrf_token"])
        self.assertEqual(logout.status_code, 200)
        self.assertIsNone(self.client.get(self.session_url).json()["username"])

    def test_cross_origin_session_is_only_shared_with_configured_origin(self):
        response = self.client.get(self.session_url, HTTP_ORIGIN="https://untrusted.example")
        self.assertNotIn("Access-Control-Allow-Origin", response)
        self.assertIn("no-store", response["Cache-Control"])
