from collections import OrderedDict

from django.test import TransactionTestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from pytest import fixture, mark

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@mark.django_db(transaction=True)
def test_snippet_serializer_should_have_attributes():
    snippet = Snippet.objects.create(code='print("hello, world")\n')

    # I want to not have to use the shell and manually check things when I
    # explore the Serializers API so here's a long test!
    serializer = SnippetSerializer(snippet)
    actual_keys = list(serializer.data.keys())
    expected_keys = ['id', 'title', 'code', 'linenos', 'language', 'style']
    assert actual_keys == expected_keys

    actual_json = JSONRenderer().render(serializer.data)
    expected_json = (
        b'{"id":3,"title":"","code":"print(\\"hello, world\\")\\n",'
        b'"linenos":false,"language":"python","style":"friendly"}')
    assert actual_json == expected_json

    ### Test/Explore Deserialization process
    # Parse a stream into native datatypes
    import io
    stream = io.BytesIO(actual_json)
    data = JSONParser().parse(stream)

    # ...then restore those native datatypes into a fully populated object
    serializer = SnippetSerializer(data=data)
    assert serializer.is_valid()

    actual_validated_data = serializer.validated_data
    expected_validated_data = OrderedDict([('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
    assert actual_validated_data == expected_validated_data

    new_snippet = serializer.save()
    assert new_snippet.pk == 4

    # We can also serialize querysets instead of model instances.
    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
    actual_snippets_count = len(serializer.data)
    assert actual_snippets_count == 4
