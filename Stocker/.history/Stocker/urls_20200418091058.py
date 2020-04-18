from django.contrib import admin
from django.urls import path
from site_users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('buy/<str:company>', views.buy, name='buy'),
    path('finishBuy/', views.finishBuy name='finishBuy'),
    path('favorite/<str:company>', views.add_to_following, name='favorite'),
    path('analysis/<str:company>', views.analysis, name='analysis'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup')
]