from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # What is the `format=html` for?
    # Because we've included format suffixed URLs such as '.json', we also need to
    # indicate on the highlight field that any format suffixed hyperlinks it returns
    # should use the '.html' suffix.
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "highlight",
            "title",
            "code",
            "linenos",
            "language",
            "style",
            "owner",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # # This is not necessary when using ModelSerializer
    # # as seen in the test but the DRF tutorial includes it?
    # # See test test_snippet_data_in_user_serializer_should_list_primary_keys
    # snippets = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Snippet.objects.all()
    # )
    # # This is doesn't seem to be necessary when using HyperlinkedModelSerializer
    # # as seen in the test but the DRF tutorial includes it?
    # snippets = serializers.HyperlinkedRelatedField(
    #     many=True, view_name="snippet-detail", read_only=True
    # )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
