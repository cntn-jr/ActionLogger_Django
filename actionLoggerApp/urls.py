from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc, logoutfunc, signupfunc, deleteUser, createAction, detailAction, errorfunc, myActionsfunc

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('topPage/', topPagefunc, name='topPage'),
    path('updateUser/', updateUserfunc, name='updateUser'),
    path('logout/', logoutfunc, name='logout'),
    path('deleteUser/', deleteUser, name='deleteUser'),
    path('createAction/', createAction, name='createAction'),
    path('detailAction/<int:pk>', detailAction, name='detailAction'),
    path('myActions/', myActionsfunc, name='myActions'),
    path('error', errorfunc, name='error'),
    path('', topPagefunc, name='topPage')
]