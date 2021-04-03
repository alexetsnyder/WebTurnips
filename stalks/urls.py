from django.urls import path
from . import views


app_name = 'stalks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='stalk_week_lists'),
    path('<int:pk>/', views.StalkWeekDetail.as_view(), name='stalk_week_detail'),
    path('newweek/', views.add_stalk_week, name='add_stalk_week'),
    path('<int:pk>/delweek', views.delete_stalk_week, name='delete_stalk_week'),
    path('<int:stalk_week_id>/newstacks/', views.add_turnip_stacks, name='add_turnip_stacks'),
    path('<int:stalk_week_id>/newprice/', views.add_day_price, name='add_day_price'),
    # path('<int:stalk_week_id>/sellstacks/', views.sell_turnip_stacks, name='sell_turnip_stacks'),
    path('newweek/validate/', views.validate_stalk_week, name='validate_stalk_week'),
]