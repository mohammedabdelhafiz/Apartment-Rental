from django.db import models

# Create your models here.
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')

# UserManager class is used to handle the validation for user registration and login
class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['Name'] = "Name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['name']):
            errors['Name'] = "Name should contain letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format"
        elif len(User.objects.filter(email = postData['email'])) > 0:
            errors['email'] = "Email already registered"
        if len(postData['pass']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['pass'] != postData['cpass']:
            errors['password_confirm'] = "Passwords do not match"
        if len(postData['phone']) < 2:
            errors['Phone'] = "Phone Number  should be at least 10 numbers "
        return errors

    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])):
            user = User.objects.get(email = postData['email'])
            if bcrypt.checkpw(postData['pass'].encode(), user.password):
                return errors
            else:
                errors['login'] = "Email OR Password incorrect"
                return errors
        else:
            errors['login'] = "Email OR Password incorrect"
            return errors

class User(models.Model):

        name = models.CharField(max_length=25)
        email = models.CharField(max_length=255)
        location = models.CharField(max_length=50)
        city = models.CharField(max_length=50)
        phone_number = models.IntegerField()
        password = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = UserManager()
        # apartments 
        # chalets

class Apartment(models.Model):
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area= models.CharField(max_length=100)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="apartments")
    cost = models.IntegerField()
    hall = models.CharField(max_length=3)
    kitchen = models.CharField(max_length=3)
    balcony = models.CharField(max_length=3)
    bedrooms = models.IntegerField()
    AC = models.CharField(max_length=3)
    img = models.ImageField(upload_to='files/apartments/', height_field=None, width_field=None, max_length=100)
    desc = models.CharField(max_length=200)
    # messages 

class Chalet(models.Model):
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area= models.CharField(max_length=100)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="chalets")
    cost = models.IntegerField()
    hall = models.CharField(max_length=3)
    kitchen = models.CharField(max_length=3)
    balcony = models.CharField(max_length=3)
    bedrooms = models.IntegerField()
    AC = models.CharField(max_length=3)
    pool = models.CharField(max_length=3)
    desc = models.CharField(max_length=200)
    img = models.ImageField(upload_to='files/chalet/', height_field=None, width_field=None, max_length=100)
    # messages 

class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    apartment = models.ForeignKey(Apartment ,on_delete=models.CASCADE , related_name='messages')
    chalet = models.ForeignKey(Chalet,on_delete=models.CASCADE , related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)














def create_user(name ,email , location , city , phone_number, password):
    return User.objects.create(name=name , email=email, location=location , phone_number=phone_number, password=password)

def get_users_list(email):
    return User.objects.filter(email=email)