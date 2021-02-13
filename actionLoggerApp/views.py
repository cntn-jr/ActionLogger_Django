from django.shortcuts import render
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import SiteUser

# Create your views here.
def signupfunc(request):
    if request.method=='GET':
        return render(request, 'signup.html', {'pageTitle':'create user'})
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
        return render(request, 'login.html', {'pageTitle':'Login'})

def logoutfunc(request):
    # ログアウト処理
    logout(request)
    return redirect('login')

@login_required #ユーザがログインしていれば
# トップページ
def topPagefunc(request):
    return render(request, 'topPage.html', {'pageTitle':'DashBoard', 'loginUser' : request.user})

@login_required
# ユーザの情報を更新
def updateUserfunc(request):
    if request.method == 'GET':
        # ページの表示
        return render(request, 'updateUser.html', {'pageTitle':'update user', 'loginUser' : request.user})
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
        return render(request, 'deleteUser.html', {})