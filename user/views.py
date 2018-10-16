from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')

def join(request):
    user = User()

    user.name = request.POST["name"]
    user.email = request.POST["email"]
    user.password = request.POST["password"]
    user.gender = request.POST["gender"]

    # models.insert((name, email, password, gender))
    user.save()

    return HttpResponseRedirect('/user/joinsuccess')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    # 객체 리턴
    results = User.objects.filter(email=request.POST["email"])\
        .filter(password=request.POST["password"])
    # user = models.get(email, password)

    # 로그인 실패!!!!!
    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 성공(처리)
    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)

    # main으로 redirect
    return HttpResponseRedirect('/')

def logout(request):
    del request.session['authuser']

    return HttpResponseRedirect('/')

def modifyform(request):
    authuser = request.session['authuser']
    data = {'user':authuser}

    return render(request, 'user/modifyform.html', data)

def modify(request):
    # user = User.objects.filter(email=request.GET['email'])
    #
    # print(user[0])
    #
    # authemail = user[0]
    # request.session['authemail'] = model_to_dict(authemail)
    #
    # change_pass = request.POST['password']
    # change_gender = request.POST['gender']
    #
    # authemail.password = change_pass
    # authemail.gender = change_gender
    #
    # authemail.save()

    result = User.objects.filter(id=request.GET['id'])

    authuser = result[0]
    request.session['authuser'] = model_to_dict(authuser)

    change_pass = request.POST['password']
    change_gender = request.POST['gender']

    authuser.password = change_pass
    authuser.gender = change_gender

    authuser.save()

    return HttpResponseRedirect('/user/modifyform')

def checkemail(request):
    results = User.objects.filter(email=request.GET['email'])

    result = {'result':len(results) == 0}       # true : not exist(사용가능)
    return JsonResponse(result)


