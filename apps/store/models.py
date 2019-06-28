from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        matching_user = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        elif len(matching_user) > 0:
            errors['email'] = "Email taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be more than 8 characters"
        if postData['password'] != postData['c_password']:
            errors['c_pass'] = "Passwords must match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        matching_user = User.objects.filter(email = postData['email'])
        if len(matching_user) == 0:
            errors['invalid'] = "Email not found"
        elif postData['password'] == "":
            errors['invalid'] = "Please enter a password"
        elif not bcrypt.checkpw(postData['password'].encode(), matching_user[0].password.encode()):
            errors['invalid'] = "Failed password"
        return errors
    
    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid"
        return errors
        

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name of Product must be at least 3 characters"
        if postData['price'] == "":
            errors['price'] = "Must Include Price"
        if len(postData['category']) < 3:
            errors['category'] = "Category must be at least 3 characters"
        if len(postData['sub_category']) < 3:
            errors['sub_category'] = "Sub Category must be at least 3 characters"
        if len(postData['brand']) < 2:
            errors['brand'] = "Brand must be at least 2 characters"
        if postData['availability'] == "":
            errors['availability'] = "Must Include Availability"
        return errors
    
    def edit_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name of Product must be at least 3 characters"
        if postData['price'] == "":
            errors['price'] = "Must Include Price"
        if len(postData['category']) < 3:
            errors['category'] = "Category must be at least 3 characters"
        if len(postData['sub_category']) < 3:
            errors['sub_category'] = "Sub Category must be at least 3 characters"
        if len(postData['brand']) < 2:
            errors['brand'] = "Brand must be at least 2 characters"
        if postData['availability'] == "":
            errors['availability'] = "Must Include Availability"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Address(models.Model):
    street = models.CharField(max_length = 255)
    unit = models.CharField(max_length = 60, null=True)
    city = models.CharField(max_length = 60)
    state = models.CharField(max_length = 60)
    zip_code = models.IntegerField()
    shipping = models.ForeignKey(User, related_name ="user_shipping_address", null = True)
    billing = models.ForeignKey(User, related_name ="user_billing_address", null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    description = models.TextField(null = True)
    category = models.CharField(max_length = 60)
    sub_category = models.CharField(max_length = 60)
    brand = models.CharField(max_length = 60)
    availability = models.CharField(max_length = 60)
    likes = models.ManyToManyField(User, related_name ="product_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ProductManager()

class Image(models.Model):
    product = models.ForeignKey(Product, related_name="image_of_product")
    image = models.FileField(upload_to='media/')

class Order(models.Model):
    products = models.ManyToManyField(Product, related_name= "orders")
    user = models.ForeignKey(User, related_name="user_order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField(null = True)
    rating = models.IntegerField(null = True)
    user = models.ForeignKey(User, related_name="reviewed_user")
    product = models.ForeignKey(Product, related_name = "reviewed_product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Checkout(models.Model):
    email = models.CharField(max_length = 255)
    token = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
