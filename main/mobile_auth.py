import json

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST


def _payload(request):
    if request.content_type != "application/json":
        return request.POST
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict) or any(not isinstance(value, str) for value in data.values()):
        return None
    return data


def _session_data(request):
    user = request.user
    return {
        "username": user.get_username() if user.is_authenticated else None,
        "can_manage_projects": user.is_authenticated and user.is_superuser,
        "csrf_token": get_token(request),
    }


@never_cache
@require_GET
def session(request):
    return JsonResponse(_session_data(request))


@never_cache
@require_POST
def sign_in(request):
    data = _payload(request)
    if data is None:
        return JsonResponse({"message": "Data login tidak valid."}, status=400)
    form = AuthenticationForm(request, data=data)
    if not form.is_valid():
        return JsonResponse({"message": "Username atau kata sandi salah."}, status=401)
    login(request, form.get_user())
    return JsonResponse(_session_data(request))


@never_cache
@require_POST
def sign_up(request):
    data = _payload(request)
    if data is None:
        return JsonResponse({"message": "Data pendaftaran tidak valid."}, status=400)
    form = UserCreationForm(data)
    if not form.is_valid():
        return JsonResponse({"errors": dict(form.errors)}, status=400)
    form.save()
    return JsonResponse({"message": "Akun berhasil dibuat."}, status=201)


@never_cache
@require_POST
def sign_out(request):
    logout(request)
    return JsonResponse(_session_data(request))
