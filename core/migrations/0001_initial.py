# Generated by Django 4.2.11 on 2025-03-03 17:09

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
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomFormula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('formula', models.TextField(help_text="Use 'ave' as variable, e.g., 'ave * 1.5'")),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('color', 'Color'), ('bw', 'Black & White')], max_length=20)),
                ('position', models.CharField(choices=[('inside', 'Inside'), ('front_page', 'Front Page'), ('back_page', 'Back Page')], max_length=20)),
                ('rate_per_sq_cm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('effective_from', models.DateField()),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.edition')),
            ],
        ),
        migrations.AddField(
            model_name='edition',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.publication'),
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('headline', models.TextField()),
                ('page', models.IntegerField()),
                ('size_sq_cm', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('type', models.CharField(blank=True, choices=[('color', 'Color'), ('bw', 'Black & White')], max_length=20)),
                ('position', models.CharField(blank=True, choices=[('inside', 'Inside'), ('front_page', 'Front Page'), ('back_page', 'Back Page')], max_length=20)),
                ('ave', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.edition')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client'),
        ),
    ]
