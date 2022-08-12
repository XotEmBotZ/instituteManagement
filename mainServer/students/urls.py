from django.urls import path
from . import views
urlpatterns=[
    # GUI
    path("",views.index),
    path("addStudent/",views.addStudent),
    path("updateStudent/",views.updateStudentFirst),
    path("updateStudent/<int:adminNo>/",views.updateStudent),
    # API
    path("api/studentCascade/",views.faceCascade.as_view()),
]