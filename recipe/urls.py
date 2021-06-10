from django.urls import path, re_path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path('',views.welcome,name='welcome'),
    path('signup/', views.signup_view, name='signup'),



    #Endpoint Apis#
    #Authentication
    path('api/register/', views.Registration.as_view(), name="register"),
    path('api/login/', views.Login.as_view(), name="login"),
    path('authlogin/', ObtainAuthToken.as_view(), name="authlogin"),

    #CategoryApis
    path('api/categories/', views.CategoryDetailList.as_view(), name='category'),
    path('api/category/post/',views.CategoryPostList.as_view(), name ='category_post'),
    path('api/category/update/<int:pk>/', views.CategoryList.as_view(), name='category_update'),
    path('api/category/delete/<int:pk>/', views.CategoryList.as_view(), name='category_delete'),
    path('api/category/get/<int:pk>/', views.CategoryList.as_view(), name='category_get'),

    #Recipes
    path('api/recipes/', views.RecipeDetailList.as_view(), name='recipe'),
    path('api/recipe/post/',views.RecipePostList.as_view(), name ='recipe_post'),
    path('api/recipe/update/<int:pk>/', views.RecipeList.as_view(), name='recipe_update'),
    path('api/recipe/delete/<int:pk>/', views.RecipeList.as_view(), name='recipe_delete'),
    path('api/recipe/get/<int:pk>/', views.RecipeList.as_view(), name='recipe_get'),
    path('api/recipe/search/<ingredient>',views.RecipeSearchList.as_view(), name='recipe_search'),

    # profile
    path('api/profile/', views.ProfileDetailsList.as_view(), name='profiles'),
    path('api/profile/update/<int:pk>/', views.ProfileList.as_view(), name='profiles_update'),
    path('api/profiles/get/<int:pk>/', views.ProfileList.as_view(), name='profiles_get'),



]