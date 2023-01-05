from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('sign_in',views.sign_in),
    path('register_user',views.register_user),
    path('sigin_in_process',views.sigin_in_process),
    path('users',views.users),
    path('users_by_admin',views.users_by_admin),
    path('add_user_page',views.add_user_page),
    path('add_user_by_admin',views.add_user_by_admin),
    path('edit_user_data_page/<int:userId>',views.edit_user_data_page),
    path('edit_data_by_admin',views.edit_data_by_admin),
    path('del_user/<int:userId>',views.del_user),
    path('change_password/<int:userId>',views.change_password),
    path('edit_description',views.edit_description),
    path('logout',views.logout),
]