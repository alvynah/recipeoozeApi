from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http  import HttpResponse
from django.contrib.auth.models import Permission
from django.shortcuts import render,HttpResponse
from django.http import Http404
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .forms import *
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import requests






# Create your views here.
@login_required()
def welcome(request):
    recipes=Recipe.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method=='POST':
        form=UploadRecipeForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user.profile
            post.save()


            return HttpResponseRedirect(request.path_info)

    else:
        form=UploadRecipeForm()
    response =requests.get('https://my-bao-server.herokuapp.com/api/breadpuns')
    puns =response.json()
    return render(request, 'recipe/index.html',{'recipes':recipes,'form':form,'users':users,'puns':puns})

   

def user_profile(request, username):
   current_user = request.user
   user_profile = get_object_or_404(User, username=username)
   if request.user == user_profile:
        return redirect('profile', username=request.user.username)
   
   recipes=user_profile.profile.recipe.all()
   
   params = {
        'recipes': recipes,
        'user_profile':user_profile,

    }
   return render(request, 'recipe/user_profile.html', params)
 
   

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            name=form.cleaned_data['fullname']
            email=form.cleaned_data['email']
            user = authenticate(username=username, password=password)
 

            login(request, user)


            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request,"welcome.html")


def profile(request, username):
    current_user = request.user.profile

    profile=Profile.objects.get(user=current_user.user)
    recipes=request.user.profile.recipe.all()
    if request.method == 'POST':
      user_form = UserUpdateForm(request.POST, instance=request.user)
      profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
      if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.profile=profile
            user.profile = request.user.profile
            user.save()

            prof = profile_form.save(commit=False)
            prof.profile=profile
            prof.profile = request.user.profile
            prof.save() 


            return HttpResponseRedirect(request.path_info)
    else:
      user_form = UserUpdateForm(instance=request.user)
      profile_form = UserProfileForm(instance=request.user.profile)

    
    params = {
        'user_form': user_form,
        'profile_form': profile_form,
        'recipes': recipes,

        }
    return render(request, 'recipe/profile.html', params)




##API endpoint##

# Register User
class Registration(APIView):
    serializer_class=UserSerializer

    def post(self, request):
      serializer=self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()

      user=serializer.data

      response={
          "data":{
              "user":dict(user),
              "status":"Success",
              "message":"User account created successfully"
          }

      }
      return Response(response, status=status.HTTP_201_CREATED)
class Login(APIView):
    serializer_login=LoginSerializer
    authentication_token=(TokenAuthentication)
    permission_classes=(IsAuthenticated,)

    def post(self, request, format=None):
        serializers=self.serializer_login(data=request.data)
        if serializers.is_valid():
            serializers.save()
            users=serializers.data

            response={
                "data":{
                    "user":dict(users),
                    "status":"Success",
                    "message":"User logged in successfully"
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 

#Category Views 

class  CategoryList(generics.ListCreateAPIView):
    def get_category(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Http404 
   
    def get(self,request,pk,format=None):
        category=self.get_category(pk)
        serializers=CategorySerializer(category)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        category=self.get_category(pk)
        serializers=CategorySerializer(category,request.data)
        if serializers.is_valid():
            serializers.save()
            category=serializers.data
            response = {
                     'data': {
                     'Category': dict(category),
                     'status': 'success',
                    'message': 'Category updated successfully',
                 }
             }
            return Response(response)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category=self.get_category(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryPostList(generics.ListCreateAPIView):

    def post(self,request,format=None):
        serializers=CategorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            category=serializers.data
            response={
                'data':{
                    'Category':dict(category),
                    'status':'success',
                    'message':'Category created successfully',
                }
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailList(APIView):
   def get(self,request,format=None):
       category=Category.objects.all()
       serializers=CategorySerializer(category,many=True)
       return Response(serializers.data)

#Recipe Views

class  RecipeList(generics.ListCreateAPIView):
    def get_recipe(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Http404 
   
    def get(self,request,pk,format=None):
        recipe=self.get_recipe(pk)
        serializers=RecipeSerializer(recipe)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        recipe=self.get_recipe(pk)
        serializers=RecipeSerializer(recipe,request.data)
        if serializers.is_valid():
            serializers.save()
            recipe=serializers.data
            response = {
                     'data': {
                     'Recipe': dict(recipe),
                     'status': 'success',
                    'message': 'Recipe updated successfully',
                 }
             }
            return Response(response)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        recipe=self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RecipePostList(generics.ListCreateAPIView):

    def post(self,request,format=None):
        serializers=RecipeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            recipe=serializers.data
            response={
                'data':{
                    'Category':dict(recipe),
                    'status':'success',
                    'message':'Recipe created successfully',
                }
            }
            return Response(response,status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailList(APIView):
   def get(self,request,format=None):
       recipe=Recipe.objects.all()
       serializers=RecipeSerializer(recipe,many=True)
       return Response(serializers.data)

class RecipeSearchList(APIView):
    def get(self,request,ingredient):
        recipe=Recipe.find_recipe(ingredient)
        serializers=RecipeSerializer(recipe, many=True)
        return Response(serializers.data)

# Profile View
class ProfileList(generics.ListCreateAPIView):
    def get_profile(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404()
    
    
    def get(self,request,pk,format=None):
        profiles=self.get_profile(pk)
        serializers=ProfileSerializer(profiles)
        return Response(serializers.data)

    def put(self,request,pk,format=None):
        profiles=self.get_profile(pk)
        serializers=ProfileSerializer(profiles,request.data)
        if serializers.is_valid():
            serializers.save()
            profiles_list=serializers.data
            response = {
                        'data': {
                        'users': dict(profiles_list),
                        'status': 'success',
                        }
                     }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailsList(APIView):
    def get(self,request,format=None):
        profiles=Profile.objects.all()
        serializers=ProfileSerializer(profiles,many=True)
        return Response(serializers.data)

@login_required
def search_results(request):
    recipes=Recipe.objects.all()

    if 'search_profile' in request.GET and request.GET["search_profile"]:
        search_term = request.GET.get("search_profile")
        searched_profiles = Recipe.search_profile(search_term)
        print(searched_profiles)
        message = f"{search_term}"
        return render(request, 'recipe/search.html', {"message":message,"profiles": searched_profiles})
    else:
        message = "You haven't searched for any recipe"
    return render(request, 'recipe/search.html', {'message': message,'recipes':recipes})