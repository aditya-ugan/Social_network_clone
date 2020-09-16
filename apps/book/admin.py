from django.contrib import admin

# Register your models here.
from .models import Location,Train,Flight,Bus,TrainFare,FlightFare,BusFare,BookFlight,BookBus,BookTrain,Passenger,Traincheckout
admin.site.register(Location)
admin.site.register(Train)
admin.site.register(TrainFare)
admin.site.register(Flight)
admin.site.register(FlightFare)
admin.site.register(Bus)
admin.site.register(BusFare)
admin.site.register(BookBus)
admin.site.register(BookTrain)
admin.site.register(BookFlight)
admin.site.register(Passenger)
admin.site.register(Traincheckout)
