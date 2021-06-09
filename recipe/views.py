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



# Create your views here.
def welcome(request):
    return HttpResponse('Welcome to the Moringa Tribune')

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
