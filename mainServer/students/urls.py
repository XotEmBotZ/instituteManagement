from django.urls import path
from . import views
urlpatterns=[
    #GUI
    path("",views.index),
    path("viewcomplaint/",views.viewComplaint.as_view()),
    path("viewstudent/",views.viewStudent),
]