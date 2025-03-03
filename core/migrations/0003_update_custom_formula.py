from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_update_coverage_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='customformula',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='customformula',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customformula',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customformula',
            name='formula',
            field=models.TextField(help_text="Use variables like 'ave', 'size', 'rate', etc. Example: 'ave * 1.5' or 'size * rate * 2'"),
        ),
    ] 