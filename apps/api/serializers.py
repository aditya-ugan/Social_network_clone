from rest_framework import serializers
from apps.book.models import Train,Bus,Flight,TrainFare,FlightFare,BusFare,BookTrain,Passenger

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model=Train
        fields='__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bus
        fields=['id','bus_name']
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flight
        fields='__all__'

class TrainFareSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrainFare
        fields='__all__'

class FlightFareSerializer(serializers.ModelSerializer):
    class Meta:
        model=FlightFare
        fields='__all__'

class BusFareSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusFare
        fields='__all__'

class BookTrainSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookTrain
        fields='__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Passenger
        fields='__all__'

