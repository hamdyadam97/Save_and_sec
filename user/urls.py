from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index_view, name='index'),

]