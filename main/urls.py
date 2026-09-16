from django.urls import path
from main.views import (
    create_project,
    delete_project,
    get_projects_json,
    show_achievements,
    show_education,
    show_experience,
    show_main,
    show_projects,
)


app_name = 'main'

urlpatterns = [
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path('achievements/', show_achievements, name='show_achievements'),
    path('education/', show_education, name='show_education'),
    path('projects/', show_projects, name='show_projects'),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
]