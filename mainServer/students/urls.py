from django.urls import path
from . import views
urlpatterns=[
    # API
    path("api/studentCascade/",views.faceCascade.as_view()),
    path("api/studentAttendance/",views.studentAttendance.as_view()),
]