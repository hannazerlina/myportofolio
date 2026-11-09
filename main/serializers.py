from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "role", "year", "description", "spotify_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def clean_text(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Isian tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_title(self, value):
        return self.clean_text(value)

    def validate_role(self, value):
        return self.clean_text(value)

    def validate_description(self, value):
        return self.clean_text(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "institution", "program", "start_year", "end_year",
            "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama institusi tidak boleh kosong.")
        return value

    def validate_program(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Program studi tidak boleh kosong.")
        return value

    def validate(self, attrs):
        # PATCH may omit either year; compare with the stored value in that case.
        start = attrs.get("start_year", getattr(self.instance, "start_year", None))
        end = attrs.get("end_year", getattr(self.instance, "end_year", None))
        if start is not None and end is not None and end < start:
            raise serializers.ValidationError({
                "end_year": "Tahun selesai tidak boleh sebelum tahun masuk."
            })
        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user in obj.starred_by.all())
