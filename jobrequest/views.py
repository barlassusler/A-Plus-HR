from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskRequestForm
from .models import JobRequest
from biko_hr.models import Job,Profile
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def task_request_list(request):
    user = request.user
    job_requests = JobRequest.objects.none()

    if user.groups.filter(name='HR').exists():
        job_requests = JobRequest.objects.all()
        print("HR user - showing all job requests")

    elif user.groups.filter(name='Manager').exists():
        profile = getattr(user, 'profile', None)
        if profile:
            job_requests = JobRequest.objects.filter(
                organization=profile.Organization,
                position_type=profile.Position
            )
            print("Manager - showing filtered job requests")

    elif user.groups.filter(name='Director').exists():
        profile = getattr(user, 'profile', None)
        if profile:
            job_requests = JobRequest.objects.filter(
                position_type=profile.Position
            )
            print("Director - showing filtered job requests")

    print(f"User: {user}, Requests: {job_requests}")
    return render(request, 'task_request_list.html', {'tasks': job_requests})

def create_task_request(request):
    if request.method == 'POST':
        form = TaskRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_request_list')  # Listeleme sayfasına yönlendir
    else:
        form = TaskRequestForm()
    tasks = Job.objects.all()
    return render(request, 'task_request_form.html', {'form': form, 'tasks': tasks})



def task_request_detail(request, pk):
    task = get_object_or_404(JobRequest, pk=pk)  # Belirli bir talebi getir
    return render(request, 'task_request_detail.html', {'task': task})