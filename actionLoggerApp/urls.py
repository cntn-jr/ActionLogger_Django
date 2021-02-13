from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc, logoutfunc, signupfunc, deleteUser

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('topPage/', topPagefunc, name='topPage'),
    path('updateUser/', updateUserfunc, name='updateUser'),
    path('logout/', logoutfunc, name='logout'),
    path('deleteUser/', deleteUser, name='deleteUser'),
]