from django.urls import path
from . import views

app_name = 'bis'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('taulak/', views.taulak, name='taulak'),
    # path('parte_hartzeak/', views.parte_hartzeak, name='parte_hartzeak'),
    # path('scatter/', views.scatter, name='scatter'),
    # path('sentimenduak/', views.sentimenduak, name='sentimenduak'),
    path('hilabete_handler/', views.hilabete_handler, name='hilabete_handler'),
]