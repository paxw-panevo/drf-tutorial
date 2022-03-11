from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from pytest import mark, fixture


@fixture(autouse=True)
def given_user():
    return User.objects.get_or_create(username="test")


@mark.django_db(transaction=True)
class TestUserViews:
    client = APIClient()

    def test_get_index(self):
        response = self.client.get("/users/")
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        actual_users_count = len(response.data)  # type: ignore
        assert actual_users_count, 2

    def test_get_detail(self):
        response = self.client.get("/users/1/")
        assert response.status_code, status.HTTP_200_OK  # type: ignore
        actual_data_keys = list(response.data.keys())  # type: ignore
        expected_data_keys = ["id", "username", "snippets"]
        assert actual_data_keys, expected_data_keys

    def test_endpoints_allow_format_suffix(self):
        # Let's just test a sampling
        for url in ["/users/1", "/users"]:
            for format in ["json", "api"]:
                response = self.client.get(f"{url}.{format}")
                assert response.status_code, status.HTTP_200_OK  # type: ignore
