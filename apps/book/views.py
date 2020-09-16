from .models import *
from.forms import BusSearch,TrainSearch,FlightSearch,CreateUser
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from apps.api.serializers import *
import requests
from random import randint
from django.forms import inlineformset_factory
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from apps.paytm import PaytmChecksum

from django.conf import settings
from django.http.response import HttpResponse
# Create your views here.
class Index(TemplateView):
    template_name = 'index.html'
def searchbus(request):
    form=BusSearch()

    context={
        'form':form,
        'user':request.user,
    }
    if request.method=='GET':
        form=BusSearch(request.GET)
        if form.is_valid():
            result=Bus.objects.filter(source__city_name__icontains=form.cleaned_data['source']).filter(destination__city_name__icontains=form.cleaned_data['destination']).filter(day=form.cleaned_data['day'])

            context['result']=result
        return render(request,'searchbus.html',context)
def searchtrain(request):
    form=TrainSearch()
    context={
        'form':form
    }
    if request.method=='GET':
        form=TrainSearch(request.GET)
        if form.is_valid():
            result=Train.objects.filter(source__city_name__icontains=form.cleaned_data['source']).filter(destination__city_name__icontains=form.cleaned_data['destination']).filter(day=form.cleaned_data['day'])
            a=request.GET['source']
            ans=TrainFare.objects.filter(name__source_id=a)
            option=TrainFare.class_choice
            context['option']=option
            context['result']=result
            a1=request.GET.get('aditya')
            context['a1']=a1
            print(a1)
        return render(request,'searchtrain.html',context)

def searchflight(request):
    form=FlightSearch()
    context={
        'form':form
    }
    if request.method=='GET':
        form=FlightSearch(request.GET)
        if form.is_valid():
            result=Flight.objects.filter(source__city_name__icontains=form.cleaned_data['source']).filter(destination__city_name__icontains=form.cleaned_data['destination']).filter(day=form.cleaned_data['day'])

            context['result']=result
        return render(request,'searchflight.html',context)


def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,'Username or password is incorrect')
    context={}
    return render(request, 'login.html', context)
def logoutpage(request):
    logout(request)
    return redirect('/')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form=CreateUser
        cust={}
        if request.method=='POST':
            form=CreateUser(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,user+' created successfully')
                return redirect('loginPage')
        context={
                    'form':form,
                }
        return render(request, 'register.html', context)
@csrf_exempt
def booknow(request,pk):
    url="http://127.0.0.1:8000/en/api/trainfare_list/"+str(pk)
    ans=requests.get(url=url).json()
    train_name=Train.objects.filter(id=ans[0]['name'])
    context={'trainname':train_name,'fare':ans[0]['fare'],'category':ans[0]['category']}
    PassengerFormSet = inlineformset_factory(BookTrain, Passenger, fields=('name', 'age'))
    formset = PassengerFormSet()
    context['form'] = formset
    if request.method=='POST':
        uniqueno = pnrgen()
        print(uniqueno)
        BookTrain.objects.create(
            user_name=request.user,
            book_type_id=pk,
            pnrno=uniqueno,
        )
        urll = "http://127.0.0.1:8000/en/api/booktrain_list/?pnrno=" + str(uniqueno)
        booktrainid = requests.get(url=urll).json()
        exp = BookTrain.objects.get(pk=booktrainid[0]['id'])
        context['pnrno'] = booktrainid[0]['pnrno']
        formset=PassengerFormSet(request.POST,instance=exp)
        if formset.is_valid():
            formset.save()
            return redirect('bookin:checkout',pnr_id=booktrainid[0]['pnrno'])
    return render(request,'book.html',context)


def checkout(request,pnr_id):
    passenger=Passenger.objects.filter(book_train__pnrno__contains=pnr_id).values_list('name',flat=True)
    trainname=Train.objects.get(trains__booktrain__pnrno__contains=pnr_id)

    trainfare=TrainFare.objects.filter(booktrain__pnrno__contains=pnr_id).values_list('fare',flat=True)

    traincategory=TrainFare.objects.filter(booktrain__pnrno__contains=pnr_id).values_list('category',flat=True)


    source=Location.objects.get(train_sources__train_name__contains=trainname)

    destination = Location.objects.get(train_destination__train_name__contains=trainname)

    context={
        'trainname':trainname,'source':source,'destination':destination,'traincategory':traincategory[0],
        'totalfare':trainfare[0]*passenger.count(),'passenger':passenger,'pnr':pnr_id
    }
    urll = "http://127.0.0.1:8000/en/api/booktrain_list/?pnrno=" + str(pnr_id)
    booktrainid = requests.get(url=urll).json()
    Traincheckout.objects.create(
        pnr_no_id=booktrainid[0]['id'],
        totalfare=trainfare[0]*passenger.count(),
        user_name=request.user,
    )


    return render(request,'checkoutpage.html',context)

def confirmation(request,statuss):

    tt=BookTrain.objects.filter(pnrno=statuss).filter(user_name_id=request.user.id).values_list('id',flat=True)
    fare=Traincheckout.objects.filter(pnr_no_id=tt[0]).values_list('totalfare')


    # import checksum generation utility
    # You can get this utility from https://developer.paytm.com/docs/checksum/


    paytmParams = dict()

    paytmParams["body"] = {
        "requestType": "Payment",
        "mid": settings.PAYTM_MERCHANT_ID,
        "websiteName": "WEBSTAGING",
        "orderId": statuss,
        "callbackUrl": settings.PAYTM_CALLBACK_URL,
        "txnAmount": {
            "value": str(fare[0][0]),
            "currency": "INR",
        },
        "userInfo": {
            "custId": request.user.username,
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]),settings.PAYTM_MERCHANT_KEY)

    paytmParams["head"] = {
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid="+settings.PAYTM_MERCHANT_ID+"&orderId="+statuss
    print(url)

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"})
    resp=response.json()
    context={
        'payment_url':settings.PAYTM_PAYMENT_GATEWAY_URL,
        'mid':settings.PAYTM_MERCHANT_ID,
        'order_id':statuss,
        'txntoken':resp['body']['txnToken'],
        'CHECKSUMHASH':resp['head']['signature'],
        'amount':'1.00',
        'website':settings.PAYTM_WEBSITE

    }
    return  render(request,'confirmation_page.html',context)


def accountdetail(request):
    history=Traincheckout.objects.filter(user_name=request.user)
    return render(request,'accounts_detail.html',{'history':history})

@csrf_exempt
def paytmresponse(request):
    order_id=''
    mid_id=''
    checksumm=''
    res_dict={}
    responseparams=request.POST
    for i in responseparams.keys():
        res_dict[i]=responseparams[i]
        if i=='ORDERID':
          order_id=responseparams[i]
        if i=='MID':
           mid_id=responseparams[i]
        if i=='CHECKSUMHASH':
            checksumm=responseparams[i]


    paytmParams = dict()

    paytmParams["MID"] = settings.PAYTM_MERCHANT_ID
    paytmParams["ORDERID"] = order_id

    # Generate checksum by parameters we have
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    checksum = PaytmChecksum.generateSignature(paytmParams, settings.PAYTM_MERCHANT_KEY)

    paytmParams["CHECKSUMHASH"] = checksumm

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/order/status"

    # for Production
    # url = "https://securegw.paytm.in/order/status"

    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
    print('response=',response)
    print('res_dict=',response)
    isVerifySignature = PaytmChecksum.verifySignature(paytmParams, settings.PAYTM_MERCHANT_KEY,checksum)
    context={}
    if isVerifySignature:
        context={'msg':'PAYEMNT SUCCESSFUL','orderid':order_id}

    else:
        context={'msg':'PAYMENT FAILED CONTACT US IF MONEY IS DEDUCTED','orderid':order_id}

    return render(request,'receipt.html',context)

def pnrgen():
    pnr=BookTrain.objects.values_list('pnrno',flat=True)
    num=randint(1,100000)
    flag=1

    while flag==1:
        if num  in pnr:
            num = randint(1, 100000)
        else:
            flag=0
            break
    return num
