from django.urls import path
from . import views
urlpatterns=[
    #GUI
    path("",views.index),
    path("viewcomplaint/",views.viewComplaint.as_view()),
    # API
    path("api/studentCascade/",views.faceCascade.as_view()),
    path("api/studentAttendance/",views.studentAttendance.as_view()),
]