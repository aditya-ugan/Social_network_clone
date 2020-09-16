from django.urls import path
from django.conf.urls import url,include
from .views import Index,searchbus,searchflight,searchtrain,booknow,checkout,confirmation,accountdetail,paytmresponse
app_name="bookin"
urlpatterns=[
    path('',Index.as_view(),name='index'),
    path('search-bus/',searchbus,name='bus-search'),
    path('search-train/',searchtrain,name='train-search'),
    path('search-flight/',searchflight,name='flight-search'),
    path('booknow/<int:pk>',booknow,name='booknow'),
    path('checkout/<str:pnr_id>',checkout,name='checkout'),
    path('confrimations/<str:statuss>/',confirmation,name='confirmation'),
    path('acountdetail/', accountdetail, name='accountDetail'),
    path('paytmresponse/',paytmresponse,name='paytmresponse'),


            ]