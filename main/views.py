from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
        ), "last_login": request.COOKIES.get("last_login", "Belum ada sesi login"),
        "faculty": "Fakultas Ilmu Komputer"
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hanna Zerlina Razaq Putri Wicaksono",
        "experience_list": Experience.objects.order_by('-started_at', 'title'),
    }
    return render(request, "experience.html", context)


def show_education(request):
    json_response = get_education_json(request)

    education_objects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    education_list = [item.object for item in education_objects]

    return render(request, "education.html", {
        "education_list": education_list,
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

@login_required(login_url="main:login")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="main:login")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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

    projects_json = serializers.serialize(
        "json",
        projects,
        use_natural_foreign_keys=True,
    )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="main:login")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@login_required(login_url="main:login")
def update_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendidikan berhasil diperbarui!")
            return redirect("main:show_education")
    else:
        form = EducationForm(instance=education)

    return render(request, "education_form.html", {
        "form": form,
        "page_title": "Edit Pendidikan",
    })
    
@login_required(login_url="main:login")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Pendidikan berhasil dihapus!")

    return redirect("main:show_education")

def get_education_json(request):
    education = Education.objects.all()
    education_json = serializers.serialize("json", education, use_natural_foreign_keys=True)

    return HttpResponse(
        education_json,
        content_type="application/json",
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat!")
            return redirect("main:login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            response = redirect("main:show_main")
            response.set_cookie(
                "last_login",
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            return response
        
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})

@require_POST
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")
