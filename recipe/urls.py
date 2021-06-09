from django.urls import path, re_path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path('',views.welcome,name='welcome'),
    #Authentication
    path('register/', views.Registration.as_view(), name="register"),
    path('login/', views.Login.as_view(), name="login"),
    path('authlogin/', ObtainAuthToken.as_view(), name="authlogin"),




]