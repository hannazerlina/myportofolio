from django.shortcuts import render

def show_main(request): # atau nama fungsi view profil kamu
    context = {
        'name': 'Hanna Zerlina Razaq Putri Wicaksono',
        'npm': '2506594692',
        'study_program': 'Sistem Informasi',
        'bio': 'Isi bio singkat kamu di sini...',
    }
    return render(request, "index.html", context)

