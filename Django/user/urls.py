from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('sign/', views.Sign_in_View.as_view(), name='sign'),   # python manage.py runserverを実行する際に, urlの後ろに'/home'をくっつける
    path('cal/', views.Calculate_View.as_view(), name='cal'), 
    path('bmi/', views.Bmi_View.as_view(), name='bmi'),
    path('game/', views.Hit_and_Blow_View.as_view(), name='game'),
    path('over/', views.Game_Over.as_view(), name='over'),
]
