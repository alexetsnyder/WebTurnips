from django.urls import path
from . import views


app_name = 'stalks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.StalkWeekDetail.as_view(), name='stalk_week_detail'),
    path('newweek/', views.form_create_stalk_week, name='create_stalk_week'),
    path('createweek/', views.new_stalk_week, name='new_stalk_week'),
]