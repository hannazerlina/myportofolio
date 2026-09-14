from datetime import date

from django.db import migrations


def add_portfolio_data(apps, schema_editor):
    alias = schema_editor.connection.alias
    Education = apps.get_model('main', 'Education')
    Project = apps.get_model('main', 'Project')
    Experience = apps.get_model('main', 'Experience')
    for institution, program, start, end in [
        ('SMA Labschool Kebayoran', 'SMA', 2022, 2025),
        ('Universitas Indonesia', 'Information Systems', 2025, None),
    ]:
        Education.objects.using(alias).get_or_create(
            institution=institution,
            defaults={'program': program, 'start_year': start, 'end_year': end},
        )
    Project.objects.using(alias).get_or_create(
        title='Skylite Musicals 2024',
        defaults={
            'role': 'Music Director',
            'year': 2024,
            'description': 'Mengarahkan musik untuk produksi teater musikal Skylite Musicals 2024, termasuk komposisi dan aransemen musik serta koordinasi dengan para penampil dan orkestra.',
            'spotify_url': 'https://open.spotify.com/track/3KkMtouqFytYnriAt3nVOT',
        },
    )
    # The existing model requires a date; only its year is displayed.
    defaults = {
        'description': 'Talent yang sedang menjalani pelatihan dan pengembangan dalam persiapan debut.',
        'started_at': date(2025, 1, 1),
        'ended_at': None,
    }
    experience = Experience.objects.using(alias).filter(title='Trinity Optima Production').first()
    if experience:
        Experience.objects.using(alias).filter(pk=experience.pk).update(**defaults)
    else:
        Experience.objects.using(alias).create(
            title='Trinity Optima Production', location='Jakarta, Indonesia',
            category='part-time', **defaults,
        )


class Migration(migrations.Migration):
    dependencies = [('main', '0003_education_project')]
    # Keep personal data when rolling back; the schema rollback removes new tables.
    operations = [migrations.RunPython(add_portfolio_data, migrations.RunPython.noop)]
