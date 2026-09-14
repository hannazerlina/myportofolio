from django.db import migrations


def clean_descriptions(apps, schema_editor):
    Experience = apps.get_model('main', 'Experience')
    experiences = Experience.objects.using(schema_editor.connection.alias)
    for experience in experiences.filter(description__contains=' menurut CV'):
        experience.description = experience.description.replace(' menurut CV', '')
        experience.save(update_fields=['description'], using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [('main', '0007_labschool_program_ipa')]
    operations = [migrations.RunPython(clean_descriptions, migrations.RunPython.noop)]
