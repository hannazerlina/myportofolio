from django.db import migrations


def update_achievements(apps, schema_editor):
    Achievement = apps.get_model('main', 'Achievement')
    records = Achievement.objects.using(schema_editor.connection.alias)
    records.filter(title='National Indonesian Student Research Olympiad', year=2024).update(
        title='Olimpiade Penelitian Siswa Indonesia (OPSI)',
        organizer='Balai Pengembangan Talenta Indonesia (BPTI), Pusat Prestasi Nasional (Puspresnas)',
    )
    records.filter(title='SkyPEX — School Business Competition', year=2023).update(
        organizer='SMA Labschool Kebayoran',
    )


class Migration(migrations.Migration):
    dependencies = [('main', '0009_achievement_organizer')]
    operations = [migrations.RunPython(update_achievements, migrations.RunPython.noop)]
