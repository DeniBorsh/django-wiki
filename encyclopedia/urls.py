from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("random/", views.rand, name="random"),
    path("new-page/", views.new_page, name="new-page"),
    path("<str:name>/edit", views.edit, name="edit")
]
