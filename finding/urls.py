from django.urls import path
from . import views

app_name = 'finding'
urlpatterns = [
    path('', views.find_person, name='find_person'),
    
    
]