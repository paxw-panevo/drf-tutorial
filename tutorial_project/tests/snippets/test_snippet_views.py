from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from pytest import mark, fixture

from snippets.models import Snippet


@fixture()
def given_user():
    user, _ = User.objects.get_or_create(username="test")
    return user


@fixture(autouse=True)
def create_data(given_user):
    Snippet.objects.create(code='foo = "bar"\n', owner=given_user)
    Snippet.objects.create(code='foo = "bar"\n', owner=given_user)


@mark.django_db(transaction=True)
class TestSnippetViews:
    client = APIClient()

    def test_get_index(self):
        response = self.client.get("/snippets/")
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        actual_snippets_count = len(response.data)  # type: ignore
        assert actual_snippets_count, 2

    def test_get_detail(self):
        response = self.client.get("/snippets/1/")
        assert response.status_code, status.HTTP_200_OK  # type: ignore
        actual_data_keys = list(response.data.keys())  # type: ignore
        expected_data_keys = ["id", "title", "code", "linenos", "language", "style"]
        assert actual_data_keys, expected_data_keys

    def test_endpoints_allow_format_suffix(self):
        # Let's just test a sampling
        for url in ["/snippets/1", "/snippets"]:
            for format in ["json", "api"]:
                response = self.client.get(f"{url}.{format}")
                assert response.status_code, status.HTTP_200_OK  # type: ignore

    def test_creating_snippet(self, given_user):
        self.client.force_authenticate(user=given_user)
        response = self.client.post("/snippets/", data={"code": 'foo = "bar"\n'})
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
