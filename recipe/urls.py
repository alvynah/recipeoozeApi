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

    #CategoryApis
    path('api/categories/', views.CategoryDetailList.as_view(), name='category'),
    path('api/category/post/',views.CategoryPostList.as_view(), name ='category_post'),
    path('api/category/update/<int:pk>/', views.CategoryList.as_view(), name='category_update'),
    path('api/category/delete/<int:pk>/', views.CategoryList.as_view(), name='category_delete'),
    path('api/category/get/<int:pk>/', views.CategoryList.as_view(), name='category_get'),

    #Recipes
    




]