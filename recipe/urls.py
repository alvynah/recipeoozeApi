from django.urls import path, re_path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns=[
    path('',views.welcome,name='welcome'),
    #Authentication
    path('register/', views.Registration.as_view(), name="register"),

]