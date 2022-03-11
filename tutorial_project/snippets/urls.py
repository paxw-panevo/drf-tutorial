from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.DefaultRouter()


format_suffix_urls = format_suffix_patterns(
    [
        path("snippets/", views.SnippetList.as_view()),
        path("snippets/<int:pk>/", views.SnippetDetail.as_view()),
        path("users/", views.UserList.as_view()),
        path("users/<int:pk>/", views.UserDetail.as_view()),
    ]
)
urlpatterns = [
    path("bapi/", include(router.urls)),
] + format_suffix_urls
