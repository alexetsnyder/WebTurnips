from django.urls import path
from . import views


app_name = 'stalks'
urlpatterns = {
    path('', views.index, name='index'),
}