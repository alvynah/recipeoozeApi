from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    prof_pic=CloudinaryField("image")
    name=models.CharField(max_length=50)
    bio=models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, search_term):
        return cls.objects.filter(user__username__icontains=search_term).all()
    def __str__(self):
        return f'{self.user.username} Profile'


class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def save_category(self):
        self.save()
    def delete_category(self):
        self.delete()

class Recipe(models.Model):
    name=models.CharField(max_length=50)
    food_pic=CloudinaryField("image")
    ingredient=models.TextField()
    time_prep=models.CharField(max_length=50)
    process=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save_recipe(self):
        self.save()
    def delete_recipe(self):
        self.delete()
    @classmethod
    def find_recipe(cls,ingredient):
        return cls.objects.filter(ingredient__icontains=ingredient)

    @classmethod
    def update_recipe(cls,id,name):
        update = cls.objects.filter(id=id).update(name=name)
        return update
