from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput
from main.models import Project, Education
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ProjectForm(ModelForm):
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError(
                "Nama proyek tidak boleh hanya berisi tag HTML."
            )

        return title

    def clean_role(self):
        role = strip_tags(self.cleaned_data["role"]).strip()

        if not role:
            raise ValidationError("Peran tidak boleh kosong.")

        return role

    def clean_description(self):
        description = strip_tags(
            self.cleaned_data["description"]
        ).strip()

        if not description:
            raise ValidationError("Deskripsi tidak boleh kosong.")

        return description
    
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
        
class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["institution", "program", "start_year", "end_year"]

        labels = {
            "institution": "Nama Sekolah / Universitas",
            "program": "Jurusan / Program Studi",
            "start_year": "Tahun Masuk",
            "end_year": "Tahun Selesai",
        }