from django.urls import path
from . import views

app_name = 'bis'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('taulak/', views.taulak, name='taulak'),
    path('parteHartzeak/', views.parteHartzeak, name='parteHartzeak'),
    path('scatter/', views.scatter, name='scatter'),
    # path('sentimenduak/', views.sentimenduak, name='sentimenduak'),
    path('hilabete_handler/', views.hilabete_handler, name='hilabete_handler'),
    path('lda/', views.lda, name="lda")
]