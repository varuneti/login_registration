from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        existing_users = User.objects.filter(email = post_data['email'])
        if len(post_data['first_name']) < 1:
            errors['first_name'] = "Name must be at least 1 character"
        if len(post_data['last_name']) < 1:
            errors['last_name'] = "Name must be at least 1 character"
        if not EMAIL_REGEX.match(post_data['email']):   
            errors['email'] = "Invalid email address!"
        if len(post_data['password']) < 4:
            errors['password'] = "Password must be at least 4 characters"
        if post_data['password'] != post_data['confirm_password']:
            errors['pw_match'] = "Password must match!"
        if len(existing_users) >= 1:
            errors['duplicate'] = "Email already exists."
        return errors

    def login_validator(self, post_data):
        errors = {}
        if len(post_data['email']) < 1:
            errors['email'] = "Email is required."
        if len(post_data['password']) < 1:
            errors['password'] = "Password is required"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __str__(self):
        return self.first_name
    

# Create your models here.
