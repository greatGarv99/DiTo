from django.shortcuts import render, redirect, get_object_or_404
from .models import Diary, ToDo

# Create your views here.

#home page
def home(request):
    return render(request,"home.html")

#Diary page
def diaryPage(request):
    """
    Reads the database and provides the data in the reverse order of time.
    (From latest to oldest)
    """
    stuff_for_front_end={
        'diaries':reversed(Diary.objects.all().reverse()),
    }
    return render(request, 'diary.html', stuff_for_front_end)


def newDiary(request):
    """
    If the data has been posted, this creates a new Diary object and saves it,
    else it renders the form for filling the details...
    """
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_author = request.POST.get('author')
        new_content = request.POST.get('content')
        Diary(title=new_title,author=new_author,content=new_content).save()
        return redirect('/diary')
    else:
        return render(request, "new_diary.html")


def delDiary(request, id):
    """
    Just deletes the required Diary object via passed id..
    """
    Diary.objects.get(id=id).delete()
    return redirect('/diary')


def editDiary(request, id):
    """
    Gets the data of the desired post and when edited provides the new values
    for the params of the post and redirects to diary page.
    """
    req_post = Diary.objects.get(id=id)
    if request.method == 'POST':
        req_post.title=request.POST.get('edit-title')
        req_post.author=request.POST.get('edit-author')
        req_post.content=request.POST.get('edit-content')
        req_post.save()
        return redirect('/diary')
    else:
        return render(request, 'edit_diary.html', {'diary':req_post})



#Todo list
def taskPage(request):
    """
    Reads the registered tasks from the database and passes it onto the 
    html page..
    """
    return render(request, 'todo_list.html', {'tasks':ToDo.objects.all()})


def newTask(request):
    """
    Save the new task if posted otherwise display the new task modal..
    """
    if request.method == 'POST':
        new_task = request.POST.get('newTask')
        ToDo(task = new_task).save()
        return redirect('/tasks')
    else:
        return render(request, 'todo_list.html', {'tasks':ToDo.objects.all(), 'new':True,})


def delTask(request, id):
    """
    Deletes the required task via passed id..
    """
    ToDo.objects.get(id=id).delete()
    return redirect('/tasks')


def editTask(request, id):
    """
    Gets the modal for editing the requitred task and changes 
    the params onto the database.. 
    """
    req_task = ToDo.objects.get(id=id)
    if request.method == 'POST':
        req_task.task = request.POST.get('editTask')
        req_task.save()
        return redirect('/tasks')
    else:
        return render(request, 'todo_list.html', {
            'tasks':ToDo.objects.all(), 
            'edit':True, 
            'edit_task':req_task,
        })