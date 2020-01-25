from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signIn, name='u_signin'),
    path('signout/', views.signOut, name='u_signout'),
    path('signup/', views.signUp, name='u_signup'),
    path('recover/', views.recoverPass, name='u_recover')
]
