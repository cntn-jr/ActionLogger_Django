from django.urls import path, include
from .views import loginfunc, topPagefunc, updateUserfunc, logoutfunc, signupfunc, deleteUser, createAction, detailAction, errorfunc, myActionsfunc, createGroupfunc, adminGroupListfunc, adminGroupDetailfunc, adminGroupDeletefunc, searchGroupfunc, groupDetailfunc, groupWithdrawalfunc, entryGroupListfunc , groupInformationListfunc, addGroupInformationfunc, groupInformationDetailfunc, adminGroupInformationfunc, adminGroupActionfunc, groupInformationfunc, adminGroupActionDetailfunc, editAction

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('topPage/', topPagefunc, name='topPage'),
    path('updateUser/', updateUserfunc, name='updateUser'),
    path('logout/', logoutfunc, name='logout'),
    path('deleteUser/', deleteUser, name='deleteUser'),
    path('createAction/', createAction, name='createAction'),
    path('detailAction/<int:pk>', editAction, name='detailAction'),
    path('myActions/', myActionsfunc, name='myActions'),
    path('createGroup/', createGroupfunc ,name='createGroup'),
    path('adminGroupList/', adminGroupListfunc, name='adminGroupList'),
    path('adminGroupDetail/<str:groupId>', adminGroupDetailfunc, name='adminGroupDetail'),
    path('adminGroupInformation/<str:groupId>', adminGroupInformationfunc, name='adminGroupInformation'),
    path('adminGroupAction/<str:groupId>', adminGroupActionfunc, name='adminGroupAction'),
    path('adminGroupAction/<str:groupId>/<int:pk>', adminGroupActionDetailfunc, name='adminGroupActionDetail'),
    path('groupInformationList/<str:groupId>', groupInformationListfunc, name='groupInformationList'),
    path('addGroupInformation/<str:groupId>', addGroupInformationfunc, name='addGroupInformation'),
    path('groupInformationDetail/<int:pk>', groupInformationDetailfunc, name='groupInformationDetail'),
    path('adminGroupDelete/<str:groupId>', adminGroupDeletefunc, name='adminGroupDelete'),
    path('searchGroup/', searchGroupfunc, name='searchGroup'),
    path('groupDetail/<str:groupId>', groupDetailfunc, name='groupDetail'),
    path('groupInoformation/<str:groupId>', groupInformationfunc, name='groupInformation'),
    path('groupWithdrawal/<str:groupId>', groupWithdrawalfunc, name='groupWithdrawal'),
    path('entryGroupList/', entryGroupListfunc, name='entryGroupList'),
    path('error', errorfunc, name='error'),
    path('', topPagefunc, name='topPage')
]