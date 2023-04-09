# Generated by Django 4.2 on 2023-04-09 09:33

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
            name='VehicleBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=30)),
                ('vehicle_type', models.CharField(choices=[('Bike | Scooter', 'Bike | Scooter'), ('Car | Jeep', 'Car | Jeep'), ('Bus | Van', 'Bus | Van'), ('Auto rickshaw', 'Auto rickshaw'), ('Truck', 'Truck')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=30, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_models', to='vehicle.vehiclebrand')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('registration_number', models.CharField(max_length=30, unique=True)),
                ('vehicle_image', models.ImageField(blank=True, null=True, upload_to='vehicle_images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_brands', to='vehicle.vehiclebrand')),
                ('vehicle_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_models', to='vehicle.vehiclemodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DrivingLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('license_file', models.FileField(upload_to='driving_license')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_driving_license', to='vehicle.vehicle')),
            ],
        ),
        migrations.AddConstraint(
            model_name='drivinglicense',
            constraint=models.UniqueConstraint(fields=('vehicle',), name='unique_driving_license_per_vehicle'),
        ),
    ]
