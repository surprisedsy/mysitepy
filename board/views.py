from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board

def list(request):
    results = Board.objects.order_by('-group_no', 'order_no')

    data = {"board_list":results}

    return render(request, 'board/list.html', data)

def view(request):
    id = request.GET["id"]

    results = Board.objects.filter(id=int(id)).order_by('-id')
    board = results[0]

    board.hit += 1
    board.save(update_fields=('hit',))

    data = {"board":board}

    return render(request, 'board/view.html', data)

def add(request):
    authuser = request.session["authuser"]
    user_id = authuser["id"]

    board = Board()

    board.title = request.POST['title']
    board.message = request.POST['message']
    board.user_id_id = user_id

    if request.method == 'POST':
        last_gno = Board.objects.aggregate(Max('group_no'))
        board.group_no = last_gno['group_no__max'] + 1

    board.save()

    return HttpResponseRedirect("/board")

def reply(request):
    return render(request, 'board/reply.html')

def replyadd(request):
    authuser = request.session["authuser"]
    user_id = authuser["id"]

    board = Board()

    board.group_no = request.GET['gno']
    board.title = request.POST['title']
    board.message = request.POST['message']
    board.user_id_id = user_id

    numbers = Board.objects.get(id=request.GET['id'])

    if numbers.order_no == 0:
        board.order_no = numbers.order_no + 1
        board.depth = numbers.depth + 1
    elif numbers.order_no >= 1:
        last_ono = Board.objects.filter(group_no=numbers.group_no).aggregate(Max('order_no'))
        board.order_no = last_ono['order_no__max'] + 1

        if board.order_no > numbers.order_no:
            board.order_no = numbers.order_no +1
            board.depth = numbers.depth +1
        else:
            last_depth = Board.objects.aggregate(Max('depth'))
            numbers.depth = last_depth['depth__max'] + 1

    board.save()

    return HttpResponseRedirect("/board")


def delete(request):
    id = request.GET['id']

    Board.objects.all().filter(id=int(id)).delete()

    return HttpResponseRedirect("/board")

def write(request):
    return render(request, 'board/write.html')

def modifyform(request):
    id = request.GET['id']

    board = Board.objects.all().filter(id=id).order_by('-id')
    result = board[0]

    data = {"board":result}
    return render(request, 'board/modify.html', data)

def modify(request):
    id = request.GET['id']
    title = request.POST['title']
    message = request.POST['message']

    board = Board.objects.all().filter(id=id).order_by('-id')
    result = board[0]

    result.title = title
    result.message = message

    result.save()

    return HttpResponseRedirect('/board')

# def pagelist(request):
#     board_list = Board.objects.all()
#     paginator = Paginator(board_list, 5)
#
#     page = request.GET.get('page')
#
#     try:
#         board = paginator.page(page)
#     except PageNotAnInteger:
#         board = paginator.page(1)
#     except EmptyPage:
#         board = paginator.page(paginator.num_pages)
#
#     data = {"board":board}
#
#     return render(request, 'board/list.html', data)