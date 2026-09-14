from django.db import migrations


def set_ipa(apps, schema_editor):
    Education = apps.get_model('main', 'Education')
    Education.objects.using(schema_editor.connection.alias).filter(
        institution='SMA Labschool Kebayoran', program='SMA',
    ).update(program='IPA')


def restore_sma(apps, schema_editor):
    Education = apps.get_model('main', 'Education')
    Education.objects.using(schema_editor.connection.alias).filter(
        institution='SMA Labschool Kebayoran', program='IPA',
    ).update(program='SMA')


class Migration(migrations.Migration):
    dependencies = [('main', '0006_cv_experience_achievements')]
    operations = [migrations.RunPython(set_ipa, restore_sma)]
