import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.conf import settings


def recipe_image_file_path(instance, filename):
    '''Generate file path for new recipe image'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


# we use the base form of register new user model from Django, we want overwrite some functions and, then we can register with password
class UserManager(BaseUserManager):

    # that **extra_fields takes any other extra functions passed in when you call create_user and pass them into extra_fields, then we can add any additional fields  
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        # we can not input password here, because the password is encrypted so we do like line 14
        ## normalize_email() helper function comes with BaseUserManager, we use it to prevent multiple signups
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using=self._db -> required for supporting multiple databases
        user.save(using=self._db)

        return user
    

    def create_superuser(self, email, password):
        """Creates and saves a new  super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""

    # unique=True -> you can only create one user with one email
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # determinate the user in the system that is active or not to allows us to deactivate the user we require
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# Tag model
class Tag(models.Model):
    '''Tag to be used for a recipe'''
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


# Ingredient model
class Ingredient(models.Model):
    '''Ingredient to be used in a recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# Recipe model
class Recipe(models.Model):
    '''Recipe object'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    
    def __str__(self):
        return self.title