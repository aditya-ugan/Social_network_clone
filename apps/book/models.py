from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


# Create your models here.
day_choice=[('MON','MON'),('TUE','TUE'),('WED','WED'),('THU','THU'),('FRI','FRI'),('SAT','SAT'),('SUN','SUN')]
class Location(models.Model):
    city_name=models.CharField(max_length=26)

    def __str__(self):
        return self.city_name


class Flight(models.Model):
        flight_name=models.CharField(max_length=30)
        source=models.ForeignKey(Location,related_name='flight_sources',on_delete=models.CASCADE)
        destination = models.ForeignKey(Location, related_name='flight_destination', on_delete=models.CASCADE)
        day=models.CharField(choices=day_choice,max_length=5)

        def __str__(self):
            return self.flight_name


class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.ForeignKey(Location, related_name='bus_sources', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='bus_destination', on_delete=models.CASCADE)
    day = models.CharField(choices=day_choice, max_length=5)

    def __str__(self):
        return self.bus_name

class Train(models.Model):
        train_name = models.CharField(max_length=30)
        source = models.ForeignKey(Location, related_name='train_sources', on_delete=models.CASCADE)
        destination = models.ForeignKey(Location, related_name='train_destination', on_delete=models.CASCADE)
        day = models.CharField(choices=day_choice, max_length=5)

        def __str__(self):
            return self.train_name

class TrainFare(models.Model):
    class_choice=[['1','1AC'],['2','2AC'],['3','3AC'],['4','SL']]
    name=models.ForeignKey(Train,related_name='trains',on_delete=models.CASCADE)
    category=models.CharField(choices=class_choice,max_length=5)
    fare=models.FloatField()

    def __str__(self):
        return self.name.train_name


class FlightFare(models.Model):
    class_choice = [('1', 'Business'), ('2', 'First Class'), ('3', 'economy')]
    name = models.ForeignKey(Flight, related_name='flights', on_delete=models.CASCADE)
    category = models.CharField(choices=class_choice, max_length=5)
    fare = models.FloatField()

    def __str__(self):
        return self.name.flight_name


class BusFare(models.Model):
    class_choice = [('1', 'AC'), ('2', 'NON-AC')]
    name = models.ForeignKey(Bus, related_name='buses', on_delete=models.CASCADE)
    category = models.CharField(choices=class_choice, max_length=5)
    fare = models.FloatField()

    def __str__(self):
        return self.name.bus_name


class BookTrain(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    book_type=models.ForeignKey(TrainFare,on_delete=models.CASCADE)
    pnrno = models.CharField(max_length=10,unique=True)
    status=models.BooleanField(default=0)
    def __str__(self):
        return self.pnrno


class Passenger(models.Model):

    name=models.CharField(max_length=26)
    age=models.IntegerField()
    book_train=models.ForeignKey(BookTrain,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Traincheckout(models.Model):
    pnr_no=models.ForeignKey(BookTrain,on_delete=models.CASCADE)
    totalfare=models.FloatField()
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.pnr_no.pnrno

class BookFlight(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    book_type = models.ForeignKey(FlightFare, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name.username
class BookBus(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    book_type=models.ForeignKey(BusFare,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name.username
