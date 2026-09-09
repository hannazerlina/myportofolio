from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Hanna Zerlina Razaq Putri Wicaksono",
        "npm": "2506594692",
        "study_program": "S1 Sistem Inforamasi",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Hanna Zerlina Razaq Putri Wicaksono",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)