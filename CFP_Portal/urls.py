from django.urls import path
from . import views

urlpatterns = [
    path('', views.helloWorld, name = 'helloWorld'),
    path('displayOrganisations', views.index, name= 'index'),
   
]