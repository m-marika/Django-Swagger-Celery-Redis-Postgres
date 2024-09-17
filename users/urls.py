from django.urls import path
from .views import UserView
from . import views


urlpatterns = [
    path('users/', views.UserView.as_view()),
]
