from rest_framework import serializers
from .models import *
from django import forms

class UserSerializer(serializers.ModelSerializer):
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  
  password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
  password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
  class Meta:
    model = User
    fields = ['username','email','password', 'password2']
    extra_kwargs = {
      "password": {'write_only': True}
    }
    
  def save(self):
    user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
    password = self.validated_data['password']
    password2 = self.validated_data['password2']
      
      
    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords must match'}) 
    
    user.set_password(password)
    user.save()
    return user

class LoginSerializer(serializers.ModelSerializer):
      username=serializers.CharField()
      password=serializers.CharField()

      class Meta:
        model = User,
        fields = ["username", "password"] 
class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = '__all__'
class RecipeSerializer(serializers.ModelSerializer):

      class Meta:
            model=Recipe
            fields="__all__"
     
      def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        return response
      

      

class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields="__all__"
    @classmethod
    def get_user(self,cls):
      return cls.user.username