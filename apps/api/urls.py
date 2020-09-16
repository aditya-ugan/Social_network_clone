from django.urls import path

from .views import  apiOverview,trainlist,trainCreate,buslist,flightlist,trainfarelist,busfarelist,flightfarelist,busfareDetail,trainfareDetail,booktrainlist,passengerlist
app_name='api'
urlpatterns=[
path('',apiOverview,name='api-overview'),
    path('train-list/',trainlist,name='Train'),
    path('train_create/',trainCreate,name='Create-train'),
    path('flight_list/',flightlist,name='flight'),
    path('bus_list/',buslist,name='bus'),
    path('trainfare_list/',trainfarelist,name='TrainFare'),
    path('busfare_list/',busfarelist,name='BusFare'),
    path('flightfare_list/',flightfarelist,name='FlightFare'),
    path('busfare_list/<int:pk>/',busfareDetail,name='busfareDetail'),
    path('trainfare_list/<int:pk>/',trainfareDetail,name='trainfareDetail'),
    path('booktrain_list/',booktrainlist,name='booktrainlist'),
    path('passenger_list',passengerlist,name='passengerlist'),

]