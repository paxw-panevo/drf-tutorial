from rest_framework import status
from rest_framework.test import APITestCase

from pytest import fixture, mark

from snippets.models import Snippet

# TODO: Let's not mix pytest and unittest
# https://stackoverflow.com/questions/68439799/typeerror-
# missing-1-required-positional-argument-while-using-pytest-fixture


@mark.django_db
class TestSnippetViews(APITestCase):
    @classmethod
    def setup_class(cls):
        Snippet.objects.create(code='foo = "bar"\n')
        Snippet.objects.create(code='foo = "bar"\n')

    def test_get_index(self):
        response = self.client.get("/snippets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_snippets_count = len(response.data)  # type: ignore
        self.assertEqual(actual_snippets_count, 2)

    def test_get_detail(self):
        response = self.client.get("/snippets/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_data_keys = list(response.data.keys())  # type: ignore
        expected_data_keys = ["id", "title", "code", "linenos", "language", "style"]
        self.assertEqual(actual_data_keys, expected_data_keys)

    def test_endpoints_allow_format_suffix(self):
        # Let's just test a sampling
        for url in ["/snippets/1", "/snippets"]:
            for format in ["json", "api"]:
                response = self.client.get(f"{url}.{format}")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
