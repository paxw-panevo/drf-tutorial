from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from pytest import mark, fixture

from snippets.models import Snippet


@fixture(autouse=True)
def create_data():
    user, _ = User.objects.get_or_create(username="test")
    Snippet.objects.create(code='foo = "bar"\n', owner=user)
    Snippet.objects.create(code='foo = "bar"\n', owner=user)


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
