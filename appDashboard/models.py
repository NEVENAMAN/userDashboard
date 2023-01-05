from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self,postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['desc']) < 3 :
            error['desc'] = "description should be at least 3 characters"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if postData['password'] != postData['confirm_password']:
            error['not_the_same'] = "the passwords are different"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return error

    def sigin_validator(self, postData):
        error = {}
        userid = User.objects.filter(email = postData['email'])
        print(postData['email'])
        if len(userid) == 0 :
            error['user_not_found'] = "user not exisit"
            return error
        user = userid[0]
        if (bcrypt.checkpw(postData['password'].encode(), user.password.encode()) != True):
            error['incorrect_password'] = "you insert password error"
        return error

    def password_validator(self,postData):
        error = {}
        special_symbols = ['$','@','#','%','^','&']
        if postData['password'] != postData['confirm_password']:
            error['not_the_same'] = "the passwords are different"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return error

# create user table
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255 , unique=True)
    password = models.CharField(max_length=255)
    desc = models.TextField()
    user_level = models.CharField(max_length=255 , default='')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# register process method
def registration(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    desc = request.POST['desc']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    if(request.POST['confirm_password'] == password) : 
        user = User.objects.create(first_name = first_name , last_name = last_name , email = email , desc = desc , password = pw_hash ,user_level = "")
        print("*** 1 ",user.id)
        print("*** 1 ",user.user_level)
        
    current_user = User.objects.get(id = user.id)
    if current_user.id == 1 :
        current_user.user_level = "admin"
        return current_user.save()
   
    else:
        current_user.user_level = "normal"
        print("*** 2 ",user.id)
        print("*** 2 ",user.user_level)
        print("*** 3",current_user.user_level)
        print(current_user.user_level)
        return current_user.save()

    

# sign in process method
def signIn(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            return loged_user.id
        else:
            return None

# get all users with their data
def get_all_users(request):
    return User.objects.all()

# get a specific user data
def get_one_user(userId):
    return User.objects.get(id=userId)

# edit user data
def edit_by_admin(userId,first_name,last_name,email,user_level):
    user = User.objects.get(id = userId)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.user_level = user_level
    return user.save()

# del user from database
def del_user_by_admin(userId):
    user = User.objects.get(id = userId)
    print(user.id)
    return user.delete()

# change password by admin
def changePassword(userId,password,confirm_password):
    user = User.objects.get(id = userId)
    pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    user.password = pw_hash
    if(confirm_password == password) : 
        return user.save()
    else:
        return None

# edit user description by user
def edit_desc(userId,desc):
    user = User.objects.get(id=userId)
    user.desc = desc
    return user.save()




    

    
    

