from django.urls import path
from . import views
urlpatterns = [
    # GUI
    path("",views.index),
    path("addcandidate/",views.addcandidate),
    path("updatecandidate/",views.updatecandidateFirst),
    path("updatecandidate/<int:adminNo>/",views.updatecandidate),
    path("addcomplaint/",views.addComplaint.as_view()),
    path("viewcomplaint/",views.viewComplaint.as_view()),
    path("editcomplaint/",views.editComplaint),
    path("viewcandidate/",views.viewcandidate),
    path("viewallbehaviornotice/",views.viewAllBehaviorNotice),
    path("editbehaviornotice/",views.editBehaviorNotice)
]
