from django.urls import path
from . import views

urlpatterns = [
    path('', views.humans, name='humans'),
    path('<int:id>', views.humans_details, name='humans_details')
]
