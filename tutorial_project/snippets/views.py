from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# The root of our API is going to be a view that supports listing all the
# existing snippets, or creating a new snippet.
# NOTE: WHAT IS THIS CSRF_EXEMPT?
# Note that because we want to be able to POST to this view from clients that
# won't have a CSRF token we need to mark the view as csrf_exempt. This isn't
# something that you'd normally want to do, and REST framework views actually
# use more sensible behavior than this, but it'll do for our purposes right now.
@csrf_exempt
def snippet_list(request):
    """List all code snippets, or create a new snippet."""
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        # TODO: WHAT HAPPENS IF I DON"T PASS MANY=True?
        serializer = SnippetSerializer(snippets, many=True)
        # TODO: safe=False says EVERYTHING must be serialized, not just dict
        # objects? Why is this argument needed instead of just assuming
        # everything is unsafe and serializing everything every time?
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# This is the view which corresponds to an individual snippet, and can be used
# to retrieve, update, or delete the snippet.
@csrf_exempt # See note on CSRF_EXEMPT above.
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    # TODO: Why is DRF not using get_object_or_404 here? Is it because that
    # raises Http404 which renders the 404 template? But what we want is a
    # response with a 404 code and no HTML body?
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
