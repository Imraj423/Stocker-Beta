from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/', login_required(views.Profile_view.as_view()), name='profile'),
    # path("login/", views.LoginView.as_view(), name="login"),
    # path('logout/', views.logoutUser, name='logout'),
]
