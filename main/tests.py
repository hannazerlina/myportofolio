from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience


class MainTest(TestCase):
    def setUp(self):
        Experience.objects.all().delete()
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            location="Universitas Indonesia",
            started_at=timezone.now().date(),
            ended_at=None,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now().date()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class EducationTests(TestCase):
    def setUp(self):
        from main.models import Education
        Education.objects.all().delete()

    def test_url_and_template(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_all_education_data_appears(self):
        from main.models import Education
        Education.objects.create(institution='Sekolah Contoh', program='SMA', start_year=2022, end_year=2025)
        Education.objects.create(institution='Kampus Contoh', program='Information Systems', start_year=2025)
        response = self.client.get(reverse('main:show_education'))
        for text in ['Sekolah Contoh', 'Kampus Contoh', 'Information Systems', '2022', '2025', 'Present']:
            self.assertContains(response, text)

    def test_empty_state(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertContains(response, 'Belum ada pendidikan yang ditambahkan.')


class ProjectTests(TestCase):
    def setUp(self):
        from main.models import Project
        Project.objects.all().delete()

    def test_url_and_template(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_all_project_data_appears(self):
        from main.models import Project
        for title in ['Musikal Satu', 'Musikal Dua']:
            Project.objects.create(title=title, role='Music Director', year=2024, description='Aransemen musik.', spotify_url='https://open.spotify.com/track/example')
        response = self.client.get(reverse('main:show_projects'))
        for text in ['Musikal Satu', 'Musikal Dua', 'Music Director', '2024', 'Aransemen musik.', 'https://open.spotify.com/track/example']:
            self.assertContains(response, text)

    def test_empty_state(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertContains(response, 'Belum ada proyek yang ditambahkan.')

    def test_optional_link_and_html_escaping(self):
        from main.models import Project
        Project.objects.create(title='<script>alert(1)</script>', role='Composer', year=2024, description='Musik')
        response = self.client.get(reverse('main:show_projects'))
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, 'Dengarkan di Spotify')


class NavigationTests(TestCase):
    def test_shared_navigation_and_footer(self):
        for page in ['show_main', 'show_experience', 'show_education', 'show_projects', 'show_achievements']:
            response = self.client.get(reverse('main:' + page))
            self.assertTemplateUsed(response, 'base.html')
            for target in ['show_main', 'show_experience', 'show_education', 'show_projects', 'show_achievements']:
                self.assertContains(response, f'href="{reverse("main:" + target)}"')
            self.assertContains(response, 'Fakultas Ilmu Komputer, Universitas Indonesia.')


class AchievementTests(TestCase):
    def setUp(self):
        from main.models import Achievement
        Achievement.objects.all().delete()

    def test_url_and_template(self):
        response = self.client.get(reverse('main:show_achievements'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'achievements.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_all_achievements_appear(self):
        from main.models import Achievement
        for title in ['Kompetisi Musik', 'Kompetisi Riset']:
            Achievement.objects.create(title=title, award='Juara 1', year=2024, description='Capaian tim.')
        response = self.client.get(reverse('main:show_achievements'))
        for value in ['Kompetisi Musik', 'Kompetisi Riset', 'Juara 1', '2024', 'Capaian tim.']:
            self.assertContains(response, value)

    def test_empty_state(self):
        response = self.client.get(reverse('main:show_achievements'))
        self.assertContains(response, 'Belum ada pencapaian yang ditambahkan.')


class CVDataTests(TestCase):
    def test_cv_data_available_after_migration(self):
        from main.models import Achievement
        self.assertEqual(Experience.objects.count(), 9)
        self.assertEqual(Achievement.objects.count(), 4)
        bywonder = Experience.objects.get(location='ByWonder')
        self.assertEqual(bywonder.ended_at.year, 2025)
        self.assertFalse(bywonder.is_ongoing)
        self.assertTrue(Experience.objects.get(title='Trinity Optima Production').is_ongoing)
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, '2024 — 2025 · Selesai')
        self.assertContains(response, 'Media Manager Volunteer')

    def test_cv_seed_does_not_duplicate_or_overwrite_edits(self):
        import importlib
        from django.apps import apps
        from django.db import connection
        from main.models import Achievement
        experience = Experience.objects.get(location='ByWonder')
        experience.description = 'Deskripsi diperbarui pemilik.'
        experience.save()
        # Recreate the title at migration 0006; migration 0010 renames it later.
        Achievement.objects.filter(title='Olimpiade Penelitian Siswa Indonesia (OPSI)').update(
            title='National Indonesian Student Research Olympiad'
        )
        migration = importlib.import_module('main.migrations.0006_cv_experience_achievements')
        from types import SimpleNamespace
        migration.add_cv_data(apps, SimpleNamespace(connection=connection))
        experience.refresh_from_db()
        self.assertEqual(experience.description, 'Deskripsi diperbarui pemilik.')
        self.assertEqual(Experience.objects.count(), 9)
        self.assertEqual(Achievement.objects.count(), 4)


class RegisterTests(TestCase):
    def test_register_form(self):
        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_creates_user_with_hashed_password(self):
        import secrets
        from django.contrib.auth import get_user_model
        password = secrets.token_urlsafe(24)
        response = self.client.post(reverse('main:register'), {
            'username': 'registration_test',
            'password1': password,
            'password2': password,
        })
        self.assertRedirects(response, reverse('main:show_main'))
        user = get_user_model().objects.get(username='registration_test')
        self.assertTrue(user.check_password(password))
        self.assertNotEqual(user.password, password)
        self.assertFalse(user.is_superuser)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_registration_does_not_create_user(self):
        from django.contrib.auth import get_user_model
        before = get_user_model().objects.count()
        response = self.client.post(reverse('main:register'), {
            'username': 'invalid_registration',
            'password1': 'short',
            'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), before)

    def test_register_requires_csrf(self):
        from django.test import Client
        response = Client(enforce_csrf_checks=True).post(reverse('main:register'), {})
        self.assertEqual(response.status_code, 403)
