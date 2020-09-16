# Generated by Django 3.0.8 on 2020-08-23 07:25

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
            name='BookTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnrno', models.CharField(max_length=10, unique=True)),
                ('status', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_name', models.CharField(max_length=30)),
                ('day', models.CharField(choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WED', 'WED'), ('THU', 'THU'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_name', models.CharField(max_length=30)),
                ('day', models.CharField(choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WED', 'WED'), ('THU', 'THU'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=26)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=30)),
                ('day', models.CharField(choices=[('MON', 'MON'), ('TUE', 'TUE'), ('WED', 'WED'), ('THU', 'THU'), ('FRI', 'FRI'), ('SAT', 'SAT'), ('SUN', 'SUN')], max_length=5)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train_destination', to='book.Location')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train_sources', to='book.Location')),
            ],
        ),
        migrations.CreateModel(
            name='TrainFare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[['1', '1AC'], ['2', '2AC'], ['3', '3AC'], ['4', 'SL']], max_length=5)),
                ('fare', models.FloatField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains', to='book.Train')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=26)),
                ('age', models.IntegerField()),
                ('book_train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookTrain')),
            ],
        ),
        migrations.CreateModel(
            name='FlightFare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'Business'), ('2', 'First Class'), ('3', 'economy')], max_length=5)),
                ('fare', models.FloatField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='book.Flight')),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_destination', to='book.Location'),
        ),
        migrations.AddField(
            model_name='flight',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_sources', to='book.Location'),
        ),
        migrations.CreateModel(
            name='BusFare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'AC'), ('2', 'NON-AC')], max_length=5)),
                ('fare', models.FloatField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buses', to='book.Bus')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_destination', to='book.Location'),
        ),
        migrations.AddField(
            model_name='bus',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_sources', to='book.Location'),
        ),
        migrations.AddField(
            model_name='booktrain',
            name='book_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.TrainFare'),
        ),
        migrations.AddField(
            model_name='booktrain',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BookFlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.FlightFare')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookBus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BusFare')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
