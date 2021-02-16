from django.shortcuts import render
import datetime
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import SiteUser, ActionLog
from .myfunc.myfunc import isTime
# Create your views here.
def signupfunc(request):
    if request.method=='GET':
        return render(request, 'signup.html', {'pageTitle':'Sign Up'})
    else:
        userId = request.POST['userId']
        password = request.POST['password']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        user=SiteUser.objects.create_user(userId, password, firstName, lastName, email)
        login(request, user)
        return redirect('topPage')

def loginfunc(request):
    if request.method == 'POST':
        # ログイン処理
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # ユーザが正しければ
            login(request, user)
            return redirect('topPage')
        else:
            return render(request, 'login.html', {'error':'ユーザ情報が正しくありません'})
    else:
        # ログインページの表示
        return render(request, 'login.html', {'pageTitle':'Log in'})

def logoutfunc(request):
    # ログアウト処理
    logout(request)
    return redirect('login')

@login_required #ユーザがログインしていれば
# トップページ
def topPagefunc(request):
    myLogs={}
    # if ActionLog.objects.filter(userId=request.user.userId):#存在していれば
    #     myLogs=ActionLog.objects.get(userId=request.user.userId)
    return render(request, 'topPage.html', {'pageTitle':'Dashboard'})

@login_required
# ユーザの情報を更新
def updateUserfunc(request):
    if request.method == 'GET':
        # ページの表示
        return render(request, 'updateUser.html', {'pageTitle':'Update'})
    else:
        # ユーザ上更新の処理
        user = request.user
        user.firstName = request.POST['firstName']
        user.lastName = request.POST['lastName']
        user.address = request.POST['address']
        user.email = request.POST['email']
        user.tel = request.POST['tel']
        user.save()
        return redirect('topPage')

@login_required
def deleteUser(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')
    else:
        return render(request, 'deleteUser.html', {'pageTitle':'Delete'})

@login_required
def createAction(request):
    if request.method=='POST':
        userId=SiteUser.objects.get(userId=request.user.userId)#ユーザIDではなくインスタンスを設定しなければならない
        departureMonth=request.POST['departureMonth']
        departureDay=request.POST['departureDay']
        departureTime=request.POST['departureTime']
        departureDate=isTime(departureMonth, departureDay, departureTime)
        homeMonth=request.POST['homeMonth']
        homeDay=request.POST['homeDay']
        homeTime=request.POST['homeTime']
        homeDate=isTime(homeMonth, homeDay, homeTime)
        if( departureDate.second == 30 | homeDate.second == 30):
            return render(request, 'createAction.html',{'pageTitle':'Create Action', 'error':'正確な日付を入力してください'})
        place=request.POST['place']
        reason=request.POST['reason']
        remarks=request.POST['remarks']
        log=ActionLog(userId=userId, place=place, reason=reason, remarks=remarks, departureTime=departureDate, goHomeTime=homeDate)#インスタンスの生成
        log.save()
        return redirect('topPage')
    else:
        #ページの表示
        return render(request, 'createAction.html',{'pageTitle':'Create Action'})