from django.urls import path
from . import views
urlpatterns=[
    path("",views.index),
    path("addStudent/",views.addStudent),
    path("updateStudent/",views.updateStudent)
]