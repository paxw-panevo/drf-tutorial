from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('snippets/', views.snippet_list),  # type: ignore
    path('snippets/<int:pk>/', views.snippet_detail), # type: ignore
]

urlpatterns = format_suffix_patterns(urlpatterns)
