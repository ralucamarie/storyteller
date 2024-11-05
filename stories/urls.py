from django.urls import path
from . import views

app_name = "stories"
urlpatterns = [
    path("", views.stories, name="stories"),
    path("<int:story_id>/", views.view_story, name="view_story"),
    path("create/", views.add_story_view, name="add_story"),
    path("<int:story_id>/update/", views.update, name="update"),
    path("<int:story_id>/delete/", views.delete, name="delete"),
    path("<int:story_id>/delete_description/<int:description_id>/", views.delete_description, name="delete_description"),
    path("<int:story_id>/edit_description/<int:description_id>/", views.edit_description, name="edit_description"),

]
