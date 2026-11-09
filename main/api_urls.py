from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    path("education/", api_views.education_list, name="education-list"),
    path("education/<int:pk>/", api_views.education_detail, name="education-detail"),
    path("education/<int:pk>/star/", api_views.education_star, name="education-star"),
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<int:pk>/", api_views.project_detail, name="project-detail"),
    path("projects/<int:pk>/star/", api_views.project_star, name="project-star"),
]
