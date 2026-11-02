from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


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
