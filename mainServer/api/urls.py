from django.urls import path
from . import views

urlpatterns = [
    #* V1
    path("v1/getfacecascade/",views.getFaceCascade),    
    path("v1/setattendance/",views.setAttendance),    
    path("v1/setfacecascade/",views.setFaceCascade),  
    path('v1/testbgjob/',views.testBgJob),
    #* V2
    path("v2/recordAttendance",views.recordAttendance),
]
