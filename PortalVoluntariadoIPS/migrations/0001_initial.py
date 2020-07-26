# Generated by Django 3.0.8 on 2020-07-22 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('age', models.IntegerField()),
                ('area_de_interesse', models.CharField(max_length=200)),
                ('descricao', models.TextField(max_length=10000)),
                ('profissao', models.CharField(max_length=200)),
                ('empresa', models.CharField(max_length=200)),
                ('gender', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=False)),
                ('morada', models.CharField(max_length=250)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_text', models.CharField(max_length=200)),
                ('empresa', models.CharField(max_length=200)),
                ('descricao', models.TextField(max_length=500)),
                ('users', models.TextField(max_length=300, null=True)),
                ('aprovado', models.BooleanField(null=True)),
                ('complete', models.BooleanField(null=True)),
                ('responsavel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PortalVoluntariadoIPS.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Avaliacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
                ('admin_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortalVoluntariadoIPS.Profile')),
                ('project_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortalVoluntariadoIPS.Project')),
            ],
        ),
    ]
