from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def index(request):
    results = Guestbook.objects.all().order_by('-id')
    data = {"guestbook_list":results}

    return render(request, 'guestbook/index.html', data)


def deleteform(request):
    guestbook = Guestbook()

    guestbook.id = request.GET['id']
    data = {"id":guestbook.id}
    return render(request, 'guestbook/deleteform.html', data)


def add(request):
    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.message = request.POST['message']

    guestbook.save()

    return HttpResponseRedirect("/guestbook")


def delete(request):
    num = request.POST['id']
    password = request.POST['password']

    Guestbook.objects.filter(id=int(num)).filter(password=password).delete()

    return HttpResponseRedirect("/guestbook")



# =================== ajax ui 꾸미기

def ajax(request):
    return render(request, 'guestbook/ajax.html')

def api_list(request):
    p = request.GET['p']
    page = (int(p)-1) * 3

    result_list = []
    results = Guestbook.objects.all().order_by('-id')[page:page+3]
    result_dict = results.values()

    for a in result_dict:
        result_list.append(a)

    data = {"results":result_list}

    return JsonResponse(data)
