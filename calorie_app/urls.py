from django.urls import path
from calorie_app.views import *

urlpatterns = [
    path('',login_view,name='login_view'),
    path('register/',register_view,name='register_view'),
    path('dashboard/',dashboard_view,name='dashboard_view'),
    path('profile/',profile_view,name='profile_view'),
    path('profile_update/',profile_update_view,name='profile_update_view'),
    path('logout/',logout_view,name='logout_view'),
    path('consumecalorielist/',calorie_consumed_list_view,name='calorie_consumed_list_view'),
    path('addcalorie/',add_consumed_calorie_view,name='add_consumed_calorie_view'),
    path('editcalorie/<int:id>/',edit_consumed_calorie_view,name='edit_consumed_calorie_view'),
    path('deletecalorie/<int:id>/',delete_consumed_calorie_view,name='delete_consumed_calorie_view'),

]