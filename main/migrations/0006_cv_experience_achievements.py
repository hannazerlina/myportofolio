from datetime import date

from django.db import migrations


def add_cv_data(apps, schema_editor):
    alias = schema_editor.connection.alias
    Experience = apps.get_model('main', 'Experience')
    Achievement = apps.get_model('main', 'Achievement')
    # First-of-month dates encode CV month precision. ByWonder's end year
    # is user-confirmed; January 1 is only a year placeholder, not an exact date.
    experiences = [
        ('Songwriter', 'Skylite Musicals 2023', 'event', date(2022, 10, 1), date(2023, 8, 1),
         'Mengomposisi dan mengaransemen lagu menggunakan Ableton dan Logic Pro serta berkolaborasi dengan anggota produksi teater musikal. Menghasilkan 3 lagu yang mencapai 10.000 stream di Spotify menurut CV.'),
        ('Sponsorship Division', 'SkyAvenue 2023', 'event', date(2022, 12, 1), date(2023, 8, 1),
         'Menegosiasikan ketentuan kerja sama sponsor, menyusun laporan capaian dan manfaat sponsorship, serta menganalisis dampak finansialnya. Tim menghimpun total Rp1 miliar dalam bentuk in-kind dan dana tunai.'),
        ('Student Council', 'Gardika Mahawira', 'organization', date(2023, 8, 1), date(2024, 8, 1),
         'Melaksanakan 21 program kerja, termasuk kegiatan olahraga dan festival musik. Kegiatan organisasi menghasilkan keuntungan sekitar Rp2 miliar atau lebih menurut CV.'),
        ('Music Director', 'Skylite Musicals 2024', 'event', date(2023, 9, 1), date(2024, 8, 1),
         'Mengarahkan produksi musik, mengomposisi dan mengaransemen lagu, berkoordinasi dengan penampil, serta menyusun jadwal latihan. Memimpin dan menjadi konduktor orkestra, dengan 16 lagu dihasilkan untuk produksi.'),
        ('Head of Events', 'SkyWalk 2024', 'event', date(2023, 12, 1), date(2024, 6, 1),
         'Memimpin perencanaan dan pelaksanaan kompetisi band, mengelola logistik serta jadwal, dan berkoordinasi dengan tim serta vendor. Mengembangkan keterlibatan audiens melalui pemasaran dan kemitraan, serta melibatkan dan mengoordinasikan musisi ternama sebagai juri.'),
        ('Ticketing Division', 'SkyAvenue 2024', 'event', date(2023, 12, 1), date(2024, 8, 1),
         'Mengelola penjualan tiket, penentuan harga, strategi pemasaran kreatif, dan pencarian platform penjualan tiket. Mencapai target 1.018 peserta dan keuntungan bersih Rp204 juta dari penjualan tiket.'),
        ('Media Manager Volunteer', 'ByWonder', 'volunteer', date(2024, 5, 1), date(2025, 1, 1),
         'Mengelola pembuatan konten dan strategi media sosial untuk memperkuat kehadiran organisasi, melibatkan audiens, serta mendukung pertumbuhan melalui komunikasi digital.'),
        ('Internship', 'Sekar Watu Damar', 'internship', date(2024, 12, 1), date(2024, 12, 1),
         'Mengembangkan konten multimedia untuk menampilkan proyek arsitektur, mengelola kampanye digital marketing, dan memperkuat kehadiran merek melalui visual storytelling untuk industri arsitektur.'),
    ]
    for title, location, category, start, end, description in experiences:
        Experience.objects.using(alias).get_or_create(
            title=title, location=location,
            defaults={'category': category, 'started_at': start, 'ended_at': end, 'description': description},
        )
    achievements = [
        ('SkyPEX — School Business Competition', 'Juara 2', 2023, 'Berperan sebagai CEO dalam tim yang meraih juara kedua kompetisi bisnis sekolah SkyPEX 2023.'),
        ('South Jakarta Band Festival', 'Juara 1', 2023, 'Meraih juara pertama pada South Jakarta Band Festival 2023.'),
        ('National Indonesian Student Research Olympiad', 'Top 30', 2024, 'Bersama rekan, menulis penelitian “Utilization of Activated Carbon from Processed Green Coconut Shell Waste (Cocos nucifera Linn var. viridis) in Carbon Pollution Filtration for Air Purifier Use.”'),
        ('Digital Poetry Musicalization Festival DKI Jakarta', 'Juara 1 & Favorite Award', 2024, 'Meraih juara pertama dan penghargaan favorit dalam festival musikalisasi puisi digital DKI Jakarta 2024.'),
    ]
    for title, award, year, description in achievements:
        Achievement.objects.using(alias).get_or_create(
            title=title, year=year, defaults={'award': award, 'description': description},
        )


class Migration(migrations.Migration):
    dependencies = [('main', '0005_achievement_alter_experience_category')]
    operations = [migrations.RunPython(add_cv_data, migrations.RunPython.noop)]
