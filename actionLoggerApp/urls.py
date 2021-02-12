from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc, logoutfunc

urlpatterns = [
    path('login/', loginfunc, name='login'),
    path('topPage/', topPagefunc, name='topPage'),
    path('updateUser/', updateUserfunc, name='updateUser'),
    path('logout/', logoutfunc, name='logout'),
]