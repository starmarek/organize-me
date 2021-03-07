import jwt
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class JWTAutTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="john", email="lennon@thebeatles.com", password="johnpassword"
        )
        self.test_user.user_permissions.set(
            [
                Permission.objects.get(name="Can add log entry"),
            ]
        )
        self.test_user.save()

        self.client = APIClient()
        self.decode_algorithm = ["HS256"]

    def test_good_credentials_get_authorization(self):
        response = self.client.post("/api/token/", {"username": "john", "password": "johnpassword"})
        self.assertEqual(response.status_code, 200)

    def test_user_object_is_in_access_token_in_get_token_pair_view(self):
        response = self.client.post("/api/token/", {"username": "john", "password": "johnpassword"})
        self.assertEqual(response.status_code, 200)

        decoded_access_token = jwt.decode(
            response.data["access"], key=settings.SECRET_KEY, algorithms=self.decode_algorithm
        )
        self.assertIn("user", decoded_access_token)
        self.assertIn("user_permissions", decoded_access_token["user"])
        self.assertIn("is_superuser", decoded_access_token["user"])
        self.assertIn("is_staff", decoded_access_token["user"])
        self.assertIn("add_logentry", decoded_access_token["user"]["user_permissions"])

    def test_user_object_is_in_access_token_in_get_refresh_token_view(self):
        response = self.client.post("/api/token/", {"username": "john", "password": "johnpassword"})
        response = self.client.post("/api/token/refresh/", {"refresh": response.data["refresh"]})
        self.assertEqual(response.status_code, 200)

        decoded_access_token = jwt.decode(
            response.data["access"], key=settings.SECRET_KEY, algorithms=self.decode_algorithm
        )
        self.assertIn("user", decoded_access_token)
        self.assertIn("user_permissions", decoded_access_token["user"])
        self.assertIn("is_superuser", decoded_access_token["user"])
        self.assertIn("is_staff", decoded_access_token["user"])
        self.assertIn("add_logentry", decoded_access_token["user"]["user_permissions"])

    def test_email_in_place_of_username_do_not_get_authorization(self):
        response = self.client.post("/api/token/", {"username": "lennon@thebeatles.com", "password": "johnpassword"})
        self.assertEqual(response.status_code, 401)

    def test_wrong_credentials_do_not_get_authorization(self):
        response = self.client.post("/api/token/", {"username": "john", "password": "password"})
        self.assertEqual(response.status_code, 401)

    # def test_access_protected_view(self):
    #     refresh = RefreshToken.for_user(self.test_user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    #     response = self.client.get("/api/reservation/")
    #     self.assertEqual(response.status_code, 200)

    # def test_fail_to_access_protected_view(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer not_a_token_at_all")

    #     response = self.client.get("/api/reservation/")
    #     self.assertEqual(response.status_code, 401)

    def test_successfully_logout_user(self):
        refresh = RefreshToken.for_user(self.test_user)
        response = self.client.post("/api/logout/", {"refresh": str(refresh)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Successful logout")

    def test_fail_to_logout_user_if_no_refresh_token_provided(self):
        response = self.client.post("/api/logout/", {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "You need to include your refresh token")

    def test_fail_to_logout_user_if_invalid_refresh_token_provided(self):
        response = self.client.post("/api/logout/", {"refresh": "not_a_token"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "You have provided an invalid token")

    def test_fail_to_use_blacklisted_refresh_token(self):
        refresh = RefreshToken.for_user(self.test_user)
        self.client.post("/api/logout/", {"refresh": str(refresh)})

        response = self.client.post("/api/token/refresh/", {"refresh": str(refresh)})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(str(response.data["detail"]), "Token is blacklisted")
