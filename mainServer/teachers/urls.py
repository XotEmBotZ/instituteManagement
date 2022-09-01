from django.urls import path
from . import views
urlpatterns = [
    # GUI
    path("",views.index),
    path("addStudent/",views.addStudent),
    path("updateStudent/",views.updateStudentFirst),
    path("updateStudent/<int:adminNo>/",views.updateStudent),
    path("addcomplaint/",views.addComplaint.as_view()),
    path("viewcomplaint/",views.viewComplaint.as_view()),
    path("editcomplaint/",views.editComplaint),
    path("viewstudent/",views.viewStudent),
]
