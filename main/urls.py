from django.urls import path
from main.views import (
    register,
    create_project,
    delete_education,
    delete_project,
    create_education,
    get_education_json,
    get_projects_json,
    show_achievements,
    show_education,
    show_experience,
    show_main,
    show_projects,
    toggle_star,
    update_education,
    login_user,
    logout_user,
    toggle_education_star,
    create_project_ajax,
    create_education_ajax,
)


app_name = 'main'

urlpatterns = [
    path("register/", register, name="register"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path('achievements/', show_achievements, name='show_achievements'),
    path('education/', show_education, name='show_education'),
    path('projects/', show_projects, name='show_projects'),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    path("education/add/", create_education, name="create_education"),
    path("education/<int:education_id>/delete/", delete_education, name="delete_education"),
    path("education/<int:education_id>/update/", update_education, name="update_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/<int:project_id>/star/", toggle_star, name="toggle_star"),
    path("education/<int:education_id>/star/", toggle_education_star, name="toggle_education_star"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
]