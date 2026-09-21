from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from main.forms import ProjectForm, EducationForm
from main.models import Achievement, Education, Experience, Project


def show_main(request):
    context = {
        "name": "Hanna Zerlina Razaq Putri Wicaksono",
        "npm": "2506594692",
        "experience_list": Experience.objects.order_by('-started_at', 'title'),
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Hi, I’m Hanna, an Information Systems student at Universitas Indonesia. "
            "I’m interested in technology, music, and the creative industry. "
            "I love exploring new ideas by learning along the way"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hanna Zerlina Razaq Putri Wicaksono",
        "experience_list": Experience.objects.order_by('-started_at', 'title'),
    }
    return render(request, "experience.html", context)


def show_education(request):
    return render(request, 'education.html', {
        'education_list': Education.objects.all(),
    })


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return render(request, 'projects.html', {
        'project_list': projects,
        'title_query': title_query,
    })


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Proyek berhasil dihapus!")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('main:show_projects'),
            })

        return redirect("main:show_projects")

    return redirect("main:show_projects")


def show_achievements(request):
    return render(request, 'achievements.html', {
        'achievement_list': Achievement.objects.all(),
    })

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Proyek berhasil ditambahkan!")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('main:show_projects'),
                })

            return redirect("main:show_projects")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': {field: [error for error in errors] for field, errors in form.errors.items()}
            }, status=400)
    else:
        form = ProjectForm()

    return render(request, "projects_form.html", {"form": form})


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def create_education(request):
    if request.method == "POST":
        form = EducationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Pendidikan berhasil ditambahkan!")
            return redirect("main:show_education")
    else:
        form = EducationForm()

    return render(request, "education_form.html", {
        "form": form,
        "page_title": "Tambah Pendidikan",
    })