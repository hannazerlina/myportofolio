import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('organization', 'Organization'),
        ('event', 'Event'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='part-time')
    started_at = models.DateField()
    ended_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Education(models.Model):
    institution = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_year', 'institution']

    def __str__(self):
        return self.institution


class Project(models.Model):
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    spotify_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return self.title


class Achievement(models.Model):
    organizer = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    award = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return self.title
