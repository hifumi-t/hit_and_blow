from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home')   # python manage.py runserverを実行する際に, urlの後ろに'/home'をくっつける
]
