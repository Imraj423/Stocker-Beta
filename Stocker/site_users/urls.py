from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.logoutUser, name='logout'),
]
