#from django.db import models


# from __future__ import unicode_literals
# from django.db import models

# Create your models here.

# class UserManager(models.Manager):
#     def validator(self, postData):
#         errors = {}
#         if (postData['first_name'].isalpha()) == False:
#             if len(postData['first_name']) < 2:
#                 errors['first_name'] = "First name can not be shorter than 2 characters"

#         if (postData['last_name'].isalpha()) == False:
#             if len(postData['last_name']) < 2:
#                 errors['last_name'] = "Last name can not be shorter than 2 characters"

#         if len(postData['email']) == 0:
#             errors['email'] = "You must enter an email"

#         if len(postData['password']) < 8:
#             errors['password'] = "Password is too short!"

#         return errors

# class User(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255,default=None)
#     password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     objects = UserManager()


# class Person(models.Model):
#     name = models.CharField(max_length=255)
#     picture = models.CharField(max_length=255)
#     status = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class File(models.Model):
#   file = models.FileField(blank=False, null=False)
#   remark = models.CharField(max_length=20)
#   timestamp = models.DateTimeField(auto_now_add=True)