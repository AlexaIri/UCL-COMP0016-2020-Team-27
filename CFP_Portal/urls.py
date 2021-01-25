from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloWorld, name = 'helloWorld'),
    path('displayOrganisations', views.index, name= 'index'),
    path('SubmissionPortal/', views.SubmissionPortal, name= 'SubmissionPortal'),
    path('SubmissionPortal/Step2', views.Submission2),
    path('SubmissionPortal/Step3', views.Submission3),
    path('SubmissionPortal/Step4', views.Submission4),

   
   
]