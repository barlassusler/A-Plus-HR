from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskRequestForm
from .models import JobRequest
from biko_hr.models import IncubationJob, Profile, Position, Candidate
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
        # Capture the dynamic form fields as well
        # position_type = request.POST.get('id_position_type')
        # position_name = request.POST.get('task_name')
        # new_position_name = request.POST.get('new_position_name', '')
        # replacement_for = request.POST.get('replacement_for', '')
        # request_reason = request.POST.get('request_reason')
        # # Ensure task_name is correctly processed (in case it's a list, it should be a single value)
        # if isinstance(position_name, list):
        #     position_name = position_name[0]  # If it's a list, take the first element
        # # Ensure task_name is correctly processed (in case it's a list, it should be a single value)
        # if isinstance(new_position_name, list):
        #     new_position_name = new_position_name[0]  # If it's a list, take the first element
        # # Ensure task_name is correctly processed (in case it's a list, it should be a single value)
        # if isinstance(replacement_for, list):
        #     replacement_for = replacement_for[0]  # If it's a list, take the first element
        # if isinstance(position_type, list):
        #     position_type= position_type[0]  # If it's a list, take the first element
        #
        # # Add these variables to the form data for saving
        # form_data = {
        #     **request.POST,
        #     'position_type': position_type,
        #     'position_name': position_name,
        #     'new_position_name': new_position_name,
        #     'replacement_for': replacement_for,
        #     'request_reason': request_reason
        # }

        form = TaskRequestForm(request.POST)
        # Capture the new position name if it exists
        new_position_name = request.POST.get('new_position_name', '').strip()

        # If a new position name is provided, save it to the Position table
        if new_position_name:
            # Check if the new position already exists to prevent duplicates
            existing_position = Position.objects.filter(position=new_position_name).first()

            # If the position doesn't exist, create a new entry in the Position table
            if not existing_position:
                Position.objects.create(position=new_position_name)
        if form.is_valid():
            form.save()
            return redirect('task_request_list')  # Redirect to the task request list page
        else:
            print(form.errors)  # Print any form validation errors for debugging
    else:
        form = TaskRequestForm()

    positions = Position.objects.all()  # Ensure positions are passed to the template
    return render(request, 'task_request_form.html', {'form': form, 'positions': positions})

def task_request_detail(request, pk):
    task = get_object_or_404(JobRequest, pk=pk)  # Belirli bir talebi getir
    assigned_candidates = task.candidates.all()  # İşe atanmış tüm adayları alın
    return render(request, 'task_request_detail.html', {'task': task, 'assigned_candidates': assigned_candidates})

def assign_candidates(request, job_request_id):
    job_request = get_object_or_404(JobRequest, id=job_request_id)
    all_candidates = Candidate.objects.all()  # Tüm adaylar
    assigned_candidates = job_request.candidates.all()  # Bu işe atanmış adaylar

    if request.method == "POST":
        selected_candidates = request.POST.get("candidates", "")  # "2,3,32" şeklinde gelir
        selected_candidates_list = selected_candidates.split(",")  # Listeye çevir: ['2', '3', '32']
        selected_candidates_list = [int(c) for c in selected_candidates_list]  # Sayılara çevir: [2, 3, 32]

        job_request.candidates.set(selected_candidates_list)  # Seçilen adayları atar
        return redirect("task_request_detail", pk=job_request.id)  # Detay sayfasına yönlendir

    return render(
        request,
        "assign_candidates.html",
        {
            "job_request": job_request,
            "all_candidates": all_candidates,
            "assigned_candidates": assigned_candidates,
        },
    )