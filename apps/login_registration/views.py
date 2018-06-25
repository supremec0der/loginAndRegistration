from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User
from django.contrib import messages
import bcrypt


def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)

def index(request):


    return render(request, 'login_registration/index.html')

def register(request):
    if request.method == "POST":

        ##### Validate the form data
        errors = User.objects.validate_registration(request.POST)

        ##### Check if errors don't exist
        if not errors:
            #####Creates the user
            hashed = bcrypt.hashpw(request.POST['register_password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST['register_firstname'], last_name = request.POST['register_lastname'], email = request.POST['register_email'], password = hashed)

            print(user)

            ##### Log in the user
            request.session['user_id'] = user.id


            return redirect(reverse('success'))
        
        #### Flash errors
        flash_errors(errors, request)



        return redirect(reverse('index'))

def login(request):
    
    if request.method == "POST":

        errors = User.objects.validate_login(request.POST)

        if not errors:
            user = User.objects.get(email=request.POST['login_email'])
            
            if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
                request.session['first_name'] = user.first_name
                request.session['id'] = user.id 
                print("password match")

                return render(request, 'login_registration/success.html')
            
            else:
                errors.append("Password do not match.")
                print("failed password")
            
            
        flash_errors(errors, request)
    
    return redirect(reverse('index'))

def success(request):

    if 'user_id' in request.session:

        context = {
            'user' : User.objects.get(id=request.session['user_id'])
        }

        
        return render(request, 'login_registration/success.html', context)

    return redirect(reverse('index'))

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('index'))
