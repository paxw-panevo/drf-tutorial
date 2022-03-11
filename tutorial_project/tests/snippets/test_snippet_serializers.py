from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from pytest import mark

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@mark.django_db(transaction=True)
def test_snippet_serializer_should_have_attributes():
    user, _ = User.objects.get_or_create(username="test")
    given_snippet = Snippet.objects.create(code='print("hello, world")\n', owner=user)

    # I want to not have to use the shell and manually check things when I
    # explore the Serializers API so here's a long test!
    serializer = SnippetSerializer(given_snippet)
    actual_keys = list(serializer.data.keys())
    expected_keys = ["id", "title", "code", "linenos", "language", "style", "owner"]
    assert actual_keys == expected_keys

    actual_json = JSONRenderer().render(serializer.data)
    expected_json = (
        b'{"id":%d,"title":"","code":"print(\\"hello, world\\")\\n",'
        b'"linenos":false,"language":"python","style":"friendly","owner":"test"}'
        % given_snippet.id
    )
    assert actual_json == expected_json

    ### Test/Explore Deserialization process
    # Parse a stream into native datatypes
    import io

    stream = io.BytesIO(actual_json)
    data = JSONParser().parse(stream)

    # ...then restore those native datatypes into a fully populated object
    # TODO: How do I get the actual object (Snippet instance)? .data IIUC is
    # serialized data.
    serializer = SnippetSerializer(data=data)
    # TODO: NOTE: GOTCHA! `When a serializer is passed a `data` keyword argument you
    # must call `.is_valid()` before attempting to access the serialized `.data`
    # representation.`
    assert serializer.is_valid()
    # TODO: NOTE: GOTCHA! `You cannot call `.save()` after accessing `serializer.data`.
    # If you need to access data before committing to the database then inspect
    # 'serializer.validated_data' instead.`
    # QUESTION: I WONDER WHY

    # Save that data we deserialized as a new Snippet
    # We can't save that data since the serializer does NOT have the owner attribute.
    # See assertions below.
    # serializer.save()
    # assert len(Snippet.objects.all()) == 2

    actual_serialized_data = serializer.data
    actual_validated_data = serializer.validated_data
    # !! serializer.data and serializer.validated_data will no longer have the "owner"
    # attribute TODO: WHY IS THAT? I think because we marked owner as read-only?
    expected_serialized_data = OrderedDict(
        {
            "title": "",
            "code": 'print("hello, world")',
            "linenos": False,
            "language": "python",
            "style": "friendly",
        }
    )
    assert actual_serialized_data == expected_serialized_data
    assert actual_validated_data == expected_serialized_data

    # We can also serialize querysets instead of model instances.
    Snippet.objects.create(code='print("hello, world")', owner=user)
    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
    actual_snippets_count = len(serializer.data)
    assert actual_snippets_count == 2
