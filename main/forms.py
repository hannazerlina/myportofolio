from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project

        fields = ["title", "role", "year", "description", "spotify_url"]

        labels = {
            "title": "Nama Proyek",
            "role": "Peran Kamu",
            "year": "Tahun",
            "description": "Deskripsi Proyek",
            "spotify_url": "Link Spotify",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Skylite Musicals 2024",
                "maxlength": 200,
            }),
            "role": TextInput(attrs={
                "placeholder": "Music Director",
            }),
            "year": NumberInput(attrs={
                "placeholder": "2024",
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan proyek dan kontribusimu",
                "rows": 3,
            }),
            "spotify_url": URLInput(attrs={
                "placeholder": "https://open.spotify.com/...",
            }),
        }