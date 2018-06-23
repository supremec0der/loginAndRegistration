from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')


class UserManager(models.Manager):
    
    def validate_registration(self, form_data):

        errors = []

        if len(form_data['register_firstname']) < 2:
            errors.append("First Name is required.")

        
        if not form_data['register_firstname'].isalpha():
            errors.append("First Name can only be letters")

        if len(form_data['register_lastname']) < 2:
            errors.append("Last Name is required.")

        if not form_data['register_lastname'].isalpha():
            errors.append("Last Name can only be letters")

        if len(form_data['register_email']) < 2:
            errors.append("Email is required.")
        
        if not EMAIL_REGEX.match(form_data['register_email']):
            errors.append("Invalid Email address.")

        if len(form_data['register_password']) < 2:
            errors.append("Password is required")
        
        if len(form_data['register_password']) < 6:
            errors.append("Password is not long enough.")
        
        if form_data['register_password'] != form_data['register_cpassword']:
            errors.append("Passwords do not match.")
        
        if User.objects.filter(email = form_data['register_email']):
            errors.append("Email is already registered")
        
        return errors
    
    def validate_login(self, form_data):
        errors = []

        if len(form_data['login_email']) <2 :
            errors.append("Email is required.")

        if len(form_data['login_password']) < 2:
            errors.append("Password is required.")
        
        return errors

        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
