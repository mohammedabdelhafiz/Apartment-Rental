from django.shortcuts import render, HttpResponse , redirect
from .models import User
from django.contrib import messages
import bcrypt
from . import models




def index(request):
    return render (request , 'index.html')

def register_user(request):
    errors = User.objects.validate_register(request.POST)
    if request.method == 'POST':
        if len(errors) >0 : 
            for key, value in errors.items():
                messages.error(request ,value)
                return redirect('/') # to be changed 
        else:
            user = request.POST
            password =user['pass']
            PW_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            models.create_user(user['name'] ,user['email'] , user['location'] , user['city'] ,user['phone']   , PW_hash )
            return redirect('/register') # to be changed

def login_user(request):
    errors = User.objects.validate_login(request.POST)
    if request.method == 'POST':
        if len(errors) >0 :
            for key, value in errors.items():
                messages.error(request ,value)
                return redirect('/')
        else:
            users_list = models.get_users_list(request.POST['password'])
            if len (users_list) == 0 :
                messages.error(request , 'please check your Email/Password')
            if not bcrypt.checkpw(request.POST['password'].encode() , users_list[0].password.encode()):
                messages.error(request , 'please check your password')
                return redirect('/')        
            request.session['user_id'] = users_list[0].id
            return redirect('/')

def success_login(request ):
    if 'user_id' not in request.session:
        messages.error(request ,'You must login to view that page')
        return redirect('/')
    else:
        context = {
            "user": models.get_user_id(request.session['user_id']),
            "reviews" : models.get_reviews,
            "books" : models.get_all_books,
        }
        return render(request ,'', context )
