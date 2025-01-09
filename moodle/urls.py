
from django.urls import path
from moodle import views

urlpatterns = [
    path('users/', views.fetch_data_for_moodle, name='fetch_connected_users'),
    path('fetch-users/', views.trigger_fetch_users, name='fetch_users'),
]