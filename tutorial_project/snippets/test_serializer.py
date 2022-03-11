from django.contrib.auth.models import User

from pytest import mark

from snippets.serializers import UserSerializer
from snippets.models import Snippet


@mark.django_db
class TestUserSerializer:
    def test_serializer_data_should_have_appropriate_attributes(self):
        user, _ = User.objects.get_or_create(username="test")
        actual_attributes = list(UserSerializer(user).data.keys())
        expected_attributes = ["id", "username", "snippets"]
        assert actual_attributes == expected_attributes

    def test_snippet_data_in_user_serializer_should_list_primary_keys(self):
        user, _ = User.objects.get_or_create(username="test")
        Snippet.objects.create(code='print("hello, world")\n', owner=user)
        actual_snippets = UserSerializer(user).data["snippets"]
        expected_snippets = [1]
        assert actual_snippets == expected_snippets

        Snippet.objects.create(code='print("hello, world")\n', owner=user)
        actual_snippets = UserSerializer(user).data["snippets"]
        expected_snippets = [1, 2]
        assert actual_snippets == expected_snippets
