from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc, logoutfunc, signupfunc, deleteUser, createAction, detailAction, errorfunc, myActionsfunc, createGroupfunc, adminGroupListfunc, adminGroupDetailfunc, adminGroupDeletefunc, entryGroupfunc

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
    path('createGroup/', createGroupfunc ,name='createGroup'),
    path('adminGroupList/', adminGroupListfunc, name='adminGroupList'),
    path('adminGroupDetail/<str:groupId>', adminGroupDetailfunc, name='adminGroupDetail'),
    path('adminGroupDelete/<str:groupId>', adminGroupDeletefunc, name='adminGroupDelete'),
    path('entryGroup/', entryGroupfunc, name='entryGroup'),
    path('error', errorfunc, name='error'),
    path('', topPagefunc, name='topPage')
]