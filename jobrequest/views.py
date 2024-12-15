from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskRequestForm
from .models import TaskRequest
from biko_hr.models import Task

def create_task_request(request):
    if request.method == 'POST':
        form = TaskRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_request_list')  # Listeleme sayfasına yönlendir
    else:
        form = TaskRequestForm()
    tasks = Task.objects.all()
    return render(request, 'task_request_form.html', {'form': form, 'tasks': tasks})

def task_request_list(request):
    tasks = TaskRequest.objects.all()
    return render(request, 'task_request_list.html', {'tasks': tasks})

def task_request_detail(request, pk):
    task = get_object_or_404(TaskRequest, pk=pk)  # Belirli bir talebi getir
    return render(request, 'task_request_detail.html', {'task': task})