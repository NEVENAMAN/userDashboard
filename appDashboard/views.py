from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,'index.html')

# render sign in page
def register(request):
    return render(request,'register.html')

# register method
def register_user(request):
    error = User.objects.register_validator(request.POST)
    if len(error) > 0 :
        for key,value in error.items():
            messages.error(request,value,extra_tags= key)
        return redirect('/register')
    else:
        if request.method == "POST":
            registration(request)
            return redirect('/sign_in')

def sign_in(request):
    return render(request,'signin.html')

# sign in by data account
def sigin_in_process(request):
    error = User.objects.sigin_validator(request.POST)
    if len(error) > 0 :
        for key,value in error.items():
            print(key)
            print(value)
            messages.error(request,value,extra_tags= key)
        return redirect('/sign_in')
    else:
        if request.method == "POST":
            print("1111")
            userId = signIn(request)
            print("2222")
            if userId != None :
                request.session['userid'] = userId
                if request.session['userId'] == 1 :
                    return redirect('/users_by_admin')
                else:
                    return redirect('/users')
            else:
                print("4444")
            return redirect('/')     

# get all users data
def users(request):
    if 'userid' in request.session:
        user = get_all_users(request)
        context = {
            "users": user,
        }
        return render(request,'users.html',context)
    else:
        return redirect('/sign_in')

# get all users data with actions by admin
def users_by_admin(request):
    if 'userid' in request.session:
        user = get_all_users(request)
        context = {
            "users": user,
        }
        return render(request,'users_by_admin.html',context)
    else:
        return redirect('/sign_in')


# add user page
def add_user_page(request):
    if 'userid' in request.session:
        return render(request,'add_user.html')
    else:
        return redirect('/sign_in')

# add user method
def add_user_by_admin(request):
    error = User.objects.register_validator(request.POST)
    if len(error) > 0 :
        for key,value in error.items():
            messages.error(request,value,extra_tags= key)
        return redirect('/add_user_page')
    else:
        if request.method == "POST":
            registration(request)
            return redirect('/users_by_admin')

# get user data
def edit_user_data_page(request,userId):
    if 'userid' in request.session:
        user = get_one_user(userId)
        context = {
            "user" : user,
        }
        return render(request,'edit_by_admin.html',context)
    else:
        return redirect('/sign_in')

# edit user data from admin in database
def edit_data_by_admin(request):
    userId = request.POST['userId']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    user_level = request.POST['user_level']
    edit_by_admin(userId,first_name,last_name,email,user_level)
    return redirect('/users_by_admin')

# delete user by admin
def del_user(request,userId):
    del_user_by_admin(userId)
    return redirect('/users_by_admin')

# change password by admin
def change_password(request,userId):
    error = User.objects.password_validator(request.POST)
    if len(error) > 0 :
        for key,value in error.items():
            messages.error(request,value,extra_tags= key)
        return redirect('/edit_user_data_page/'+ str(userId))
    else:
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        changePassword(userId,password,confirm_password)
        return redirect('/users_by_admin')

# edit user description by user
def edit_description(request,userId):
    desc = request.POST['desc']
    edit_desc(userId,desc)
    return redirect('/users')

# logout method
def logout(request):
    request.session.flush()
    return redirect('/')
