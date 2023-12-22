from django.core.checks import messages
from django.shortcuts import redirect, render, HttpResponse
from .models import *
import bcrypt
from django.contrib import messages

def index(request):

    return render(request, "index.html")
def success(request):
    context = {
        'this_user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'success.html', context)

def register(request): # POST
    if request.method != "POST":
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(5)).decode()
    new_user= User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw        
    )
    request.session['user_id']= new_user.id
    return redirect('/success')

def login(request):
    if request.method != 'POST':
        return redirect("/")
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for value in errors.values():
            messages.error(request, value)
            return redirect("/")
    this_user = User.objects.filter(email = request.POST['email'])[0]
    if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
        request.session['user_id'] = this_user.id
        return redirect("/success")
    messages.error(request, "Please enter a valid email and password.")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')


# Create your views here.
