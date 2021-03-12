from django.urls import path
from . import views


app_name = 'stalks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.StalkWeekDetail.as_view(), name='stalk_week_detail'),
]