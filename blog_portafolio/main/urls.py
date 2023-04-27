from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.IndexView.as_view(), name='home'),
]
