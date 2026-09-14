from django.db import migrations


def update_organizers(apps, schema_editor):
    Achievement = apps.get_model('main', 'Achievement')
    records = Achievement.objects.using(schema_editor.connection.alias)
    records.filter(title='Olimpiade Penelitian Siswa Indonesia (OPSI)', year=2024).update(
        organizer='Kemendikbudristek — melalui BPTI dan Puspresnas',
    )
    # Organizer confirmed by the portfolio owner.
    records.filter(title='Digital Poetry Musicalization Festival DKI Jakarta', year=2024).update(
        organizer='Kemendikbudristek',
    )


class Migration(migrations.Migration):
    dependencies = [('main', '0010_verified_achievement_organizers')]
    operations = [migrations.RunPython(update_organizers, migrations.RunPython.noop)]
