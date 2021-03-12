from django.shortcuts import render
import datetime
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import SiteUser, ActionLog, MgtGroup
from .myfunc.myfunc import isTime, dateFormat
from django.utils.datastructures import MultiValueDictKeyError
from urllib.parse import urlencode
import re
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
        userIdRegex='^[a-zA-Z0-9_-]{4,10}$'
        if(not re.match(userIdRegex, userId)):
            return render(request, 'signup.html', {'error':'ユーザIDは、英数、ハイフンまたはアンダーバーのみです。'})
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
    myLogs=ActionLog.objects.filter(userId=request.user.userId).order_by('submitTime').reverse()[:5]
    myLogsCount = myLogs.count()
    for log in myLogs:
        log.departureTime = dateFormat(log.departureTime)
        log.goHomeTime = dateFormat(log.goHomeTime)
    return render(request, 'topPage.html', {'pageTitle':'Dashboard', 'myLogs':myLogs, 'myLogsCount':myLogsCount})

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
    logInfo = {}
    if request.method=='POST':
        #POST通信の場合
        userId=SiteUser.objects.get(userId=request.user.userId)#ユーザIDではなくインスタンスを設定しなければならない
        departureMonth=request.POST['departureMonth']
        departureDay=request.POST['departureDay']
        departureTime=request.POST['departureTime']
        departureDate=isTime(departureMonth, departureDay, departureTime)
        homeMonth=request.POST['homeMonth']
        homeDay=request.POST['homeDay']
        homeTime=request.POST['homeTime']
        homeDate=isTime(homeMonth, homeDay, homeTime)
        place=request.POST['place']
        reason=request.POST['reason']
        remarks=request.POST['remarks']
        if( (departureDate.second == 30 | homeDate.second == 30) | (departureDate > homeDate)):
            #正当な値（日付）が入力されなかった場合
            logInfo = { 'departureMonth' : departureMonth,'departureDay' : departureDay,'departureTime' : departureTime,'homeMonth' : homeMonth,'homeDay' : homeDay,'homeTime' : homeTime,'place' : place,'reason' : reason,'remarks' : remarks }
            return render(request, 'createAction.html',{'pageTitle':'Create Action', 'error':'正確な日付を入力してください', 'logInfo':logInfo})
        #新しいオブジェクトの生成
        log=ActionLog(userId=userId, place=place, reason=reason, remarks=remarks, departureTime=departureDate, goHomeTime=homeDate)#インスタンスの生成
        log.save()
        return redirect('topPage')
    else:
        #ページの表示
        return render(request, 'createAction.html',{'pageTitle':'Create Action', 'logInfo':logInfo})

@login_required
def myActionsfunc(request):
    myActions = ActionLog.objects.filter(userId=request.user.userId).order_by('submitTime').reverse()
    myActionsCount = myActions.count() #自分の行動履歴の総数
    pageCount = int( ( myActions.count() - 1 + 10 ) / 10 )  #自分の行動履歴の全ページ数(10件ごと)
    if(myActionsCount == 0):
        pageCount = 1
    redirect_url = reverse('myActions') #nameからURLパターンを取得
    try:
        page = int(request.GET['page'])
        if(page < 1):
            parameters = urlencode({'page': 1}) #パラメータをURLで使える形に
            url = f'{redirect_url}?{parameters}' #URL
            return redirect(url)
        if(page > pageCount):
            parameters = urlencode({'page': pageCount})
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
    except ValueError:
        parameters = urlencode({'page': 1})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    except MultiValueDictKeyError:
        parameters = urlencode({'page': 1})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    myActions = myActions[page*10-10:page*10-1]
    previousPage = page - 1#前ページ
    if(previousPage < 1):
        previousPage = 1
    nextPage = page + 1#次ページ
    if(nextPage > pageCount):
        nextPage = pageCount
    for log in myActions:
        log.departureTime = dateFormat(log.departureTime)
        log.goHomeTime = dateFormat(log.goHomeTime)
    return render(request, 'myActions.html', {'pageTitle':'My Actions', 'myActions':myActions, 'pageCount':range(pageCount), 'myActionsCount':myActionsCount, 'previousPage':previousPage, 'nextPage':nextPage})

@login_required
def detailAction(request, pk):
    log = ActionLog.objects.get(pk=pk)
    log.departureTime = dateFormat(log.departureTime)
    log.goHomeTime = dateFormat(log.goHomeTime)
    logUser = SiteUser.objects.get(userId=log.userId)
    if(request.user == logUser):#オブジェクトの比較　ユーザIDの比較ではうまくいかない
        return render(request, 'detailAction.html', {'pageTitle':'Detail Action', 'log':log})
    else:
        return redirect('error')

@login_required
def createGroupfunc(request):
    if(request.method == 'POST'):   #グループの作成処理
        groupId=request.POST['groupId']
        groupName=request.POST['groupName']
        adminUser=request.user
        groupIdRegex='^[a-zA-Z0-9_-]{8,12}$'
        if(not re.match(groupIdRegex, groupId)):
            return render(request, 'createGroup.html', {'error':'グループIDは、英数、ハイフンまたはアンダーバーのみです。'})
        group=MgtGroup(groupId=groupId, groupName=groupName, adminUserId=adminUser)
        group.save()
        return redirect('topPage')
    else:   #グループ作成画面の表示
        return render(request, 'createGroup.html', {'pageTitle':"CREATE GROUP"})

@login_required
def adminGroupListfunc(request):
    manageGroup = MgtGroup.objects.filter(adminUserId=request.user.userId)
    return render(request, 'manageGroupList.html', {'pageTitle':'GROUP LIST','mgtGroup':manageGroup})

@login_required
def adminGroupDetailfunc(request, groupId):
    manageGroup = MgtGroup.objects.get(groupId=groupId)
    if(not (SiteUser.objects.get(userId=manageGroup.adminUserId) == request.user)):
        return redirect('error')
    return render(request, 'manageGroupDetail.html', {'pageTitle':'GROUP DETAIL','mgtGroup':manageGroup})

@login_required
def adminGroupDeletefunc(request, groupId):
    manageGroup = MgtGroup.objects.get(groupId=groupId)
    if(not (SiteUser.objects.get(userId=manageGroup.adminUserId) == request.user)):
        return redirect('error')
    if(request.method == 'POST'):
        manageGroup.delete()
        return redirect('adminGroupList')
    else:
        return render(request, 'manageGroupDelete.html', {'pageTitle':'GROUP DELETE','mgtGroup':manageGroup})

def errorfunc(request):
    return render(request, 'error.html', {'pageTitle':'ERROR'})