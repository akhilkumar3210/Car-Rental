# Generated by Django 5.1.6 on 2025-03-11 06:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_delete_rented'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tot_price', models.IntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.booking')),
                ('buy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.buy')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cars')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
