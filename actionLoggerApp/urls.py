from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc

urlpatterns = [
    path('login/', loginfunc, name='login'),
    path('topPage/', topPagefunc, name='topPage'),
    path('updateUser/', updateUserfunc, name='updateUser'),
]