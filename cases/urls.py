from django.urls import path
from . import views

app_name = 'cases'
urlpatterns = [
    path('add_case', views.add_case, name='add_case'),
    
]