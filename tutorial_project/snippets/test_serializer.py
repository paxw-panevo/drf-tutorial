from django.contrib.auth.models import User

from pytest import mark

from snippets.serializers import UserSerializer


@mark.django_db
class TestUserSerializer:
    def test_serializer_data_should_have_appropriate_attributes(self):
        user, _ = User.objects.get_or_create(username="test")
        actual_attributes = list(UserSerializer(user).data.keys())
        expected_attributes = ["id", "username", "snippets"]
        assert actual_attributes == expected_attributes
