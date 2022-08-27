from django.urls import path
from . import views

urlpatterns = [
    path("getfacecascade/",views.getFaceCascade),    
    path("setattendance/",views.setAttendance),    
    path("setfacecascade/",views.setFaceCascade),    
]
