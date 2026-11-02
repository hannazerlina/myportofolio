from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<int:pk>/", api_views.project_detail, name="project-detail"),
    path("projects/<int:pk>/star/", api_views.project_star, name="project-star"),
]
