from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
def loginfunc(request):
    if request.method == 'POST':
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
        return render(request, 'login.html', {'pageTitle':'Login'})

@login_required #ユーザがログインしていれば
def topPagefunc(request):
    return render(request, 'topPage.html', {'pageTitle':'DashBoard'})

@login_required
def updateUserfunc(request):
    return render(request, 'updateUser.html', {'pageTitle':'updateUser'})
