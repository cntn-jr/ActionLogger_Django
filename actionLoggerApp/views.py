from django.shortcuts import render
import datetime
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import SiteUser, ActionLog, MgtGroup, EntryGroup, GroupInformation
from .myfunc.myfunc import isTime, dateFormat
from django.utils.datastructures import MultiValueDictKeyError
from urllib.parse import urlencode
import re
from django.db.models import Q
import datetime
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
        if(not re.match('\S', place)):
            #場所と理由が入力されなかった場合
            logInfo = { 'departureMonth' : departureMonth,'departureDay' : departureDay,'departureTime' : departureTime,'homeMonth' : homeMonth,'homeDay' : homeDay,'homeTime' : homeTime,'place' : place,'reason' : reason,'remarks' : remarks }
            return render(request, 'createAction.html',{'pageTitle':'Create Action', 'error':'正確に入力してください', 'logInfo':logInfo})
        if(not re.match('\S', reason)):
            #場所と理由が入力されなかった場合
            logInfo = { 'departureMonth' : departureMonth,'departureDay' : departureDay,'departureTime' : departureTime,'homeMonth' : homeMonth,'homeDay' : homeDay,'homeTime' : homeTime,'place' : place,'reason' : reason,'remarks' : remarks }
            return render(request, 'createAction.html',{'pageTitle':'Create Action', 'error':'正確に入力してください', 'logInfo':logInfo})
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
def editAction(request, pk):
    log = ActionLog.objects.get(pk=pk)
    logUser = SiteUser.objects.get(userId=log.userId)
    if request.method == 'GET':
        departureMonth = log.departureTime.month
        departureDay = log.departureTime.day
        departureHour = log.departureTime.hour
        homeMonth = log.goHomeTime.month
        homeDay = log.goHomeTime.day
        homeHour = log.goHomeTime.hour
        if(request.user == logUser):#オブジェクトの比較　ユーザIDの比較ではうまくいかない
            return render(request, 'editAction.html', {'pageTitle':'Detail Action', 'log':log, 'dMonth':departureMonth, 'dDay':departureDay, 'dHour':departureHour, 'hMonth':homeMonth, 'hDay':homeDay, 'hHour':homeHour,})
        else:
            return redirect('error')
    else:
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
            redirect('detailAction', pk)
        if(not re.match('\S', place)):
            #場所と理由が入力されなかった場合
            redirect('detailAction', pk)
        if(not re.match('\S', reason)):
            #場所と理由が入力されなかった場合
            redirect('detailAction', pk)
        log.departureTime = departureDate
        log.goHomeTime = homeDate
        log.place = place
        log.reason = reason
        log.remarks = remarks
        log.save()
        return redirect('detailAction',pk)


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
    if(request.method == 'GET'):
        #お知らせ
        groupInformation = GroupInformation.objects.filter(groupId=groupId).order_by('pk').reverse()[:5]
        groupInformationCount = groupInformation.count()
        return render(request, 'manageGroupDetail.html', {'pageTitle':'GROUP DETAIL','mgtGroup':manageGroup,  'groupInformation':groupInformation, 'groupInformationCount':groupInformationCount, 'detailNav':'active'})
    else:
        groupName = request.POST['groupName']
        manageGroup.groupName = groupName
        manageGroup.save()
        return redirect('adminGroupDetail',manageGroup.groupId)

@login_required
def adminGroupInformationfunc(request, groupId):
    manageGroup = MgtGroup.objects.get(groupId=groupId)
    if(not (SiteUser.objects.get(userId=manageGroup.adminUserId) == request.user)):
        return redirect('error')
    #お知らせ
    groupInformation = GroupInformation.objects.filter(groupId=groupId).order_by('pk').reverse()[:5]
    groupInformationCount = groupInformation.count()
    return render(request, 'manageGroupInformation.html', {'pageTitle':'GROUP INFORMATION','mgtGroup':manageGroup,  'groupInformation':groupInformation, 'groupInformationCount':groupInformationCount, 'informationNav': 'active'})

@login_required
def adminGroupActionfunc(request, groupId):
    manageGroup = MgtGroup.objects.get(groupId=groupId)
    if(not (SiteUser.objects.get(userId=manageGroup.adminUserId) == request.user)):
        return redirect('error')
    #グループの参加者の行動履歴
    actions = []
    participants = EntryGroup.objects.filter(groupId=manageGroup.groupId)
    allActions = ActionLog.objects.all().order_by('submitTime').reverse()
    for action in allActions:
        for man in participants:
            if action.userId == man.userId:
                actions.append(action)

    actionsCount = len(actions) #行動履歴の総数
    pageCount = int( ( actionsCount - 1 + 10 ) / 10 )  #自分の行動履歴の全ページ数(10件ごと)
    if(actionsCount == 0):
        #０になった場合
        pageCount = 1

    redirect_url = reverse('adminGroupAction',kwargs={'groupId':groupId}) #nameからURLパターンを取得
    try:
        page = int(request.GET['page'])
        #try文は、不正な値への対策
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
    actions = actions[page*10-10:page*10-1]

    #前ページ
    previousPage = page - 1
    if(previousPage < 1):
        previousPage = 1
    #次ページ
    nextPage = page + 1
    if(nextPage > pageCount):
        nextPage = pageCount

    for log in actions:
        log.departureTime = dateFormat(log.departureTime)
        log.goHomeTime = dateFormat(log.goHomeTime)

    return render(request, 'manageGroupAction.html', {'pageTitle':'GROUP INFORMATION','mgtGroup':manageGroup, 'actions':actions, 'actionNav': 'active', 'pageCount':range(pageCount), 'actionsCount':actionsCount, 'previousPage':previousPage, 'nextPage':nextPage})

@login_required
def adminGroupActionDetailfunc(request, groupId, pk):
    manageGroup = MgtGroup.objects.get(groupId=groupId)
    action = ActionLog.objects.get(pk=pk)
    if(not (SiteUser.objects.get(userId=manageGroup.adminUserId) == request.user)):
        return redirect('error')
    action.departureTime = dateFormat(action.departureTime)
    action.goHomeTime = dateFormat(action.goHomeTime)
    return render(request, 'manageGroupActionDetail.html', {'pageTitle':'ACTION LOG', 'mgtGroup':manageGroup,'action':action, 'actionNav': 'active', })

@login_required
def groupInformationListfunc(request, groupId):
    group = MgtGroup.objects.get(groupId=groupId)
    information = GroupInformation.objects.filter(groupId=groupId).order_by('pk').reverse()
    if(SiteUser.objects.get(userId=group.adminUserId) == request.user):
        informationCount = information.count() #自分の行動履歴の総数
        pageCount = int( ( information.count() - 1 + 10 ) / 10 )  #自分の行動履歴の全ページ数(10件ごと)
        if(informationCount == 0):
            pageCount = 1
        redirect_url = reverse('groupInformationList', kwargs={'groupId':groupId}) #nameからURLパターンを取得
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
        information = information[page*10-10:page*10-1]
        previousPage = page - 1#前ページ
        if(previousPage < 1):
            previousPage = 1
        nextPage = page + 1#次ページ
        if(nextPage > pageCount):
            nextPage = pageCount
        return render(request, 'groupInformationList.html', {'pageTitle':'Group Infromation List', 'information':information ,'pageCount':range(pageCount), 'informationCount':informationCount, 'previousPage':previousPage, 'nextPage':nextPage, 'group':group})
    if(EntryGroup.objects.filter(groupId=groupId, userId=request.user.userId).exists()):
        informationCount = information.count() #自分の行動履歴の総数
        pageCount = int( ( information.count() - 1 + 10 ) / 10 )  #自分の行動履歴の全ページ数(10件ごと)
        if(informationCount == 0):
            pageCount = 1
        redirect_url = reverse('groupInformationList', kwargs={'groupId':groupId}) #nameからURLパターンを取得
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
        information = information[page*10-10:page*10-1]
        previousPage = page - 1#前ページ
        if(previousPage < 1):
            previousPage = 1
        nextPage = page + 1#次ページ
        if(nextPage > pageCount):
            nextPage = pageCount
        return render(request, 'groupInformationList.html', {'pageTitle':'Group Infromation List', 'information':information ,'pageCount':range(pageCount), 'informationCount':informationCount, 'previousPage':previousPage, 'nextPage':nextPage, 'group':0})
    return redirect('error')

@login_required
def addGroupInformationfunc(request,groupId):
    if request.method == 'GET':
        return render(request, 'addGroupInformation.html', {'pageTitle':'ADD GROUP INFORMATION'})
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleRegex = '^[\S]{1,30}$'
        contentRegex = '^[\S]{1,200}$'
        if(not re.match(titleRegex, title)):
            return redirect('addGroupInformation', groupId)
        if(not re.match(contentRegex, content)):
            return redirect('addGroupInformation', groupId)
        information = GroupInformation(groupId=MgtGroup.objects.get(groupId=groupId), informationTitle=title, informationText=content)
        information.save()
        return redirect('adminGroupDetail', groupId)

@login_required
def groupInformationDetailfunc(request, pk):
    information = GroupInformation.objects.get(pk=pk)
    group = MgtGroup.objects.get(groupId=information.groupId.groupId)
    if(request.method == 'GET'):
        if(SiteUser.objects.get(userId=group.adminUserId) == request.user):
            #管理者の場合
            return render(request, 'groupInformationEdit.html', {'pageTitle':'Group Infromation List', 'information':information})
        if(EntryGroup.objects.filter(groupId=group.groupId, userId=request.user.userId).exists()):
            #参加者の場合
            information = GroupInformation.objects.get(pk=pk)
            return render(request, 'groupInformationDetail.html', {'pageTitle':'Group Infromation List', 'information':information})
        return redirect('error')
    else:
        information = GroupInformation.objects.get(pk=pk)
        title = request.POST['title']
        content = request.POST['content']
        titleRegex = '^[\S]{1,30}$'
        contentRegex = '^[\S]{1,200}$'
        if(not re.match(titleRegex, title)):
            return redirect('groupInformationDetail', information.pk)
        if(not re.match(contentRegex, content)):
            return redirect('groupInformationDetail', information.pk)
        information.informationTitle = title
        information.informationContent = content
        information.save()
        return redirect('groupInformationDetail', pk)

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

@login_required
def searchGroupfunc(request):
    if(request.method == 'POST'):
        groupId = request.POST['groupId']
        group = MgtGroup.objects.filter(groupId=groupId)
        if(group.count == 0):
            return render(request, 'searchGroup.html', {'pageTitle':'ENTRY GROUP','error':'検索結果はヒットしませんでした'})
        adminUserId = MgtGroup.objects.get(groupId=groupId).adminUserId
        if(request.user == SiteUser.objects.get( userId=adminUserId )):
            return render(request, 'searchGroup.html', {'pageTitle':'ENTRY GROUP','error':'検索結果はヒットしませんでした'})
        adminUserName = SiteUser.objects.get( userId=adminUserId ).firstName + ' ' + SiteUser.objects.get( userId=adminUserId ).lastName
        return render(request, 'searchGroup.html', {'pageTitle':'SEARCH GROUP RESULT','groups':group, 'adminUserName': adminUserName})
    else:
        return render(request, 'searchGroup.html', {'pageTitle':'ENTRY GROUP',})

@login_required
def groupDetailfunc(request, groupId):
    if(request.method == 'POST'):
        entryGroup = EntryGroup(groupId=MgtGroup.objects.get(groupId=groupId), userId=request.user)
        entryGroup.save()
        return redirect('groupDetail',groupId)
    else:
        entryGroup = MgtGroup.objects.get(groupId=groupId)
        #グループの管理者であれば
        if(request.user == SiteUser.objects.get(userId=entryGroup.adminUserId)):
            return redirect('adminGroupDetail', entryGroup.groupId)
        #グループに参加していれば
        if(EntryGroup.objects.filter(groupId=groupId,userId=request.user.userId).exists()):
            adminUserId = entryGroup.adminUserId
            #グループの管理者名
            adminUserName = SiteUser.objects.get(userId=adminUserId).firstName + ' ' + SiteUser.objects.get(userId=adminUserId).lastName
            #グループの参加人数
            entryGroupNum = EntryGroup.objects.filter(groupId=groupId).count()
            #お知らせ
            groupInformation = GroupInformation.objects.filter(groupId=groupId).order_by('pk').reverse()[:5]
            groupInformationCount = groupInformation.count()
            return render(request, 'groupDetail.html', {'group':entryGroup,'adminUserName':adminUserName,'groupNum':entryGroupNum, 'detailNav':'active'})
        #グループへの参加ページ
        else:
            return render(request, 'entryGroup.html', {'group':entryGroup,})
    return redirect('error')

@login_required
def groupInformationfunc(request, groupId, ):
    if(request.method == 'POST'):
        entryGroup = EntryGroup(groupId=MgtGroup.objects.get(groupId=groupId), userId=request.user)
        entryGroup.save()
        return redirect('groupDetail',groupId)
    else:
        entryGroup = MgtGroup.objects.get(groupId=groupId)
        #グループの管理者であれば
        if(request.user == SiteUser.objects.get(userId=entryGroup.adminUserId)):
            return redirect('adminGroupDetail', entryGroup.groupId)
        #グループに参加していれば
        if(EntryGroup.objects.filter(groupId=groupId,userId=request.user.userId).exists()):
            #お知らせ
            groupInformation = GroupInformation.objects.filter(groupId=groupId).order_by('pk').reverse()[:5]
            groupInformationCount = groupInformation.count()
            return render(request, 'groupInformation.html', {'group':entryGroup,'groupInformation':groupInformation, 'groupInformationCount':groupInformationCount, 'informationNav':'active'})
        #グループへの参加ページ
        else:
            return render(request, 'entryGroup.html', {'group':entryGroup,})
    return redirect('error')

@login_required
def groupWithdrawalfunc(request, groupId):
    if(request.method == 'GET'):
        #参加していれば
        if(EntryGroup.objects.filter(userId=request.user.userId, groupId=groupId).exists()):
            return render(request, 'groupWithdrawal.html', {'group':MgtGroup.objects.get(groupId=groupId)})
        #参加していなければ
        else:
            return redirect('searchGroup')
    else:
        #グループ退会処理
        entriedGroup = EntryGroup.objects.get(userId=request.user.userId, groupId=groupId)
        entriedGroup.delete()
        return redirect('searchGroup')

@login_required
def entryGroupListfunc(request):
    entryGroup = EntryGroup.objects.filter(userId=request.user.userId)
    return render(request, 'entryGroupList.html', {'pageTitle':'ENTRY GROUP LIST', 'entryGroup':entryGroup})

def errorfunc(request):
    return render(request, 'error.html', {'pageTitle':'ERROR'})