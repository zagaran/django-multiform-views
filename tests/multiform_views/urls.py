from django.urls import path
from django.views.generic import TemplateView

from .views import JournalistAndCommentFormsView, MultipleCommentsFormsView

urlpatterns = [
    path("/journalist/form", JournalistAndCommentFormsView.as_view()),
    path("/journalist/detail", TemplateView.as_view(template_name="multiform_views/dummy.html")),

    path("/comment/form", MultipleCommentsFormsView.as_view()),
    path("/comment/<foo>", TemplateView.as_view(template_name="multiform_views/dummy.html")),
    path("/comments", TemplateView.as_view(template_name="multiform_views/dummy.html")),
]

