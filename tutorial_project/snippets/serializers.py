from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


class UserSerializer(serializers.ModelSerializer):
    # # This is not necessary as seen in the test but the DRF tutorial includes it?
    # # See test test_snippet_data_in_user_serializer_should_list_primary_keys
    # snippets = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Snippet.objects.all()
    # )

    class Meta:
        model = User
        fields = ["id", "username", "snippets"]
