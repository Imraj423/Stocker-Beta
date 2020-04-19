from django.contrib import admin
from django.urls import path, include
from site_users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('buy/<str:company>', views.buy, name='buy'),
    path('finalize/<str:ticker>', views.finish_buy, name='finalize'),
    path('favorite/<str:company>', views.add_to_following, name='favorite'),
    path('', include('site_users.urls'), name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout')

]
