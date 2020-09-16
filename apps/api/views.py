from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.serializers import TrainSerializer,FlightSerializer,BusSerializer,TrainFareSerializer,FlightFareSerializer,BusFareSerializer,BookTrainSerializer,PassengerSerializer
from apps.book.models import *
@api_view(['GET'])
def apiOverview(request):
    api_urls={
        "Train":'train-list',
        "Create-train":'train_create',
        "Flight":'flight_list',
        "bus":'bus_list',
        'TrainFare':"trainfare_list",
        'BusFare': "busfare_list",
        'BUSFARE_Detail':'busfareDeatail',
        'FlightFare': "flightfare_list",
        "booktrain":"booktrain_list",
        "passenger":"passenger_list",


    }
    return Response(api_urls)

@api_view(['GET'])
def trainlist(request):

    trains=Train.objects.all()
    serializer=TrainSerializer(trains,many=True)
    return  Response(serializer.data)

@api_view(['POST'])
def trainCreate(request):
    serializer=TrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return  Response(serializer.data)

@api_view(['GET'])
def buslist(request):
    bus=Bus.objects.all()
    serializer=BusSerializer(bus,many=True)
    return  Response(serializer.data)

@api_view(['GET'])
def flightlist(request):
    flights=Flight.objects.all()
    serializer=FlightSerializer(flights,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def trainfarelist(request):
    name = request.query_params.get('name')
    category = request.query_params.get('category')
    id_name = request.query_params.get('id')
    fare = request.query_params.get('fare')
    trainfare = TrainFare.objects.all()
    if name and category:
        trainfare = trainfare.filter(name_id=name).filter(category=category)
    if name and category and id_name and fare :
        trainfare=trainfare.filter(name_id=name).filter(category=category).filter(id=id_name).filter(fare=fare)
    serializer=TrainFareSerializer(trainfare,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def flightfarelist(request):
    flightfare=FlightFare.objects.all()
    serializer=FlightFareSerializer(flightfare,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def busfarelist(request):
    name = request.query_params.get('name')

    busfare=BusFare.objects.all()
    serializer=BusFareSerializer(busfare,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def busfareDetail(request,pk):
    busf_id=request.GET(pk=pk)
    busfare=BusFare.objects.all()
    if busf_id:
        busfare=BusFare.objects.filter(id=busf_id)
    serializer=BusFareSerializer(busfare,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def trainfareDetail(request,pk):

    trainfare=TrainFare.objects.filter(id=pk)
    serializer=TrainFareSerializer(trainfare,many=True)
    return  Response(serializer.data)
@api_view(['GET'])
def booktrainlist(request):

    booklist=BookTrain.objects.all()
    pnr = request.query_params.get('pnrno')
    if pnr:
        booklist=booklist.filter(pnrno=pnr)
    serializer=BookTrainSerializer(booklist,many=True)
    return  Response(serializer.data)

@api_view(['GET'])
def passengerlist(request):

    passenger=Passenger.objects.all()
    serializer=PassengerSerializer(passenger,many=True)
    return  Response(serializer.data)