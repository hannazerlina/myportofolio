from django.urls import path
from main.views import show_main, show_experience, show_education, show_projects, show_achievements

app_name = 'main'

urlpatterns = [
    path('achievements/', show_achievements, name='show_achievements'),
    path('education/', show_education, name='show_education'),
    path('projects/', show_projects, name='show_projects'),
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
]