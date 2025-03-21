from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import date
from django.contrib import messages

from .forms import TaskRequestForm
from .models import *
from biko_hr.models import IncubationJob, Profile, Position, Application
from .models import JobRequest
from biko_hr.models import IncubationJob, Profile, Position, Candidate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def task_request_list(request):
    user = request.user
    job_requests = JobRequest.objects.none()
    filter_type = request.GET.get('filter', 'all')  # Filtre tipi

    # Kullanıcı profili ve lokasyon
    profile = getattr(user, 'profile', None)
    user_location = profile.Location if profile and profile.Location else None
    print(f"User: {user}, Profile: {profile}, Location: {user_location}")

    if user.groups.filter(name='HR').exists():
        job_requests = JobRequest.objects.all()
        print("HR user - showing all job requests")

    elif user.groups.filter(name='Manager').exists():
        if profile:
            job_requests = JobRequest.objects.filter(
                location=profile.Location,
                organization=profile.Organization
            )
            print("Manager - showing filtered job requests")

    elif user.groups.filter(name='Director').exists():
        if profile:
            job_requests = JobRequest.objects.filter(
                organization=profile.Organization
            )
            print("Director - showing filtered job requests")

    # Kullanıcı lokasyonuna göre filtreleme
    if filter_type == 'user_location' and user_location:
        job_requests = job_requests.filter(location=user_location)
        print(f"Filtering by location: {user_location}, Results: {job_requests.count()}")

    print(f"User: {user}, Requests: {job_requests.count()}")
    return render(request, 'task_request_list.html', {'tasks': job_requests})

@login_required
def task_request_list_hr(request):
    user = request.user
    job_requests = JobRequest.objects.none()
    filter_type = request.GET.get('filter', 'all')  # Filtre tipi

    # Kullanıcı profili ve lokasyon
    profile = getattr(user, 'profile', None)
    user_location = profile.Location if profile and profile.Location else None
    print(f"User: {user}, Profile: {profile}, Location: {user_location}")

    if user.groups.filter(name='HR').exists():
        job_requests = JobRequest.objects.filter(
            request_status_organization_manager="Accepted"
        )
    elif user.groups.filter(name='Director').exists():
        if profile:
            job_requests = JobRequest.objects.filter(
                organization=profile.Organization,
                request_status_organization_manager="Accepted"
            )
            print("Director - showing filtered job requests")

    # Kullanıcı lokasyonuna göre filtreleme
    if filter_type == 'user_location' and user_location:
        job_requests = job_requests.filter(location=user_location)
        print(f"Filtering by location: {user_location}, Results: {job_requests.count()}")

    print(f"User: {user}, Requests: {job_requests.count()}")
    return render(request, 'task_request_list_hr.html', {'tasks': job_requests})

@login_required
def task_request_list_org(request):
    user = request.user
    job_requests = JobRequest.objects.none()
    filter_type = request.GET.get('filter', 'all')  # Filtre tipi

    # Kullanıcı profili ve lokasyon
    profile = getattr(user, 'profile', None)
    user_location = profile.Location if profile and profile.Location else None
    print(f"User: {user}, Profile: {profile}, Location: {user_location}")

    if user.groups.filter(name='Director').exists():
        if profile:
            job_requests = JobRequest.objects.filter(
                request_status_organization_manager="Pending",
                organization=profile.Organization
            )

    # Kullanıcı lokasyonuna göre filtreleme
    if filter_type == 'user_location' and user_location:
        job_requests = job_requests.filter(location=user_location)
        print(f"Filtering by location: {user_location}, Results: {job_requests.count()}")

    print(f"User: {user}, Requests: {job_requests.count()}")
    return render(request, 'task_request_list_director.html', {'tasks': job_requests})

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
                # new_position = Position.objects.create(position=new_position_name) ## TODO: update the above line with this logic.
                # JobRequest.position_name = new_position
        if form.is_valid():
            form.save()
            return redirect('task_request_list')  # Redirect to the task request list page
        else:
            print(form.errors)  # Print any form validation errors for debugging
    else:
        form = TaskRequestForm()

    positions = Position.objects.all()  # Ensure positions are passed to the template
    organizations = Organization.objects.all()  # Ensure positions are passed to the template
    locations = Location.objects.all()  # Ensure positions are passed to the template
    return render(request, 'task_request_form.html', {'form': form, 'positions': positions, "locations": locations, "organizations": organizations})



@login_required
def task_request_detail(request, pk):
    task = get_object_or_404(JobRequest, pk=pk)
    assigned_candidates = task.candidates.all().prefetch_related(
        'application_set__job'
    )
    
    return render(request, 'task_request_detail.html', {
        'task': task,
        'assigned_candidates': assigned_candidates,
    })

@login_required
def assign_candidates(request, job_request_id):
    job_request = get_object_or_404(JobRequest, id=job_request_id)
    all_candidates = Candidate.objects.all()

    if request.method == 'POST':
        candidate_ids = request.POST.get('candidates', '').split(',')
        if candidate_ids and candidate_ids[0]:  # Check if there are any candidates selected
            # Create or get IncubationJob for this JobRequest
            incubation_job, created = IncubationJob.objects.get_or_create(
                position=job_request.position_name,
                organization=job_request.organization,
                defaults={
                    'title': job_request.position_name.position if job_request.position_name else job_request.new_position_name,
                    'description': job_request.description or '',
                    'required_skills': job_request.special_requirements or '',
                    'status': 'Active',
                    'preferred_locations': job_request.location.location,
                    'department': job_request.organization.organization
                }
            )

            # Create Application entries for each candidate
            for candidate_id in candidate_ids:
                candidate = get_object_or_404(Candidate, id=int(candidate_id))
                
                # Check if application already exists
                application, created = Application.objects.get_or_create(
                    candidate=candidate,
                    job=incubation_job,
                    assigned_by=request.user,
                    defaults={
                        'application_date': date.today(),
                        'status': 'HR Assesment'  # Initial status
                    }
                )
                
                # Add candidate to job_request.candidates if not already added
                job_request.candidates.add(candidate)

            messages.success(request, f'{len(candidate_ids)} candidates have been assigned successfully.')
            return redirect('task_request_detail', pk=job_request_id)
        else:
            messages.error(request, 'No candidates were selected.')

    context = {
        'job_request': job_request,
        'all_candidates': all_candidates,
        'assigned_candidates': job_request.candidates.all()
    }
    return render(request, 'assign_candidates.html', context)

@login_required
def accept_task_request(request, pk):
    try:
        task_request = JobRequest.objects.get(pk=pk)
        task_request.request_status_organization_manager = "Accepted"
        task_request.save()
        print(f"Task {pk} has been accepted.")
    except JobRequest.DoesNotExist:
        print(f"Task {pk} does not exist.")
    return redirect('task_request_list')  # Redirect back to the task request list

@login_required
def view_assigned_candidates(request, job_request_id):
    job_request = get_object_or_404(JobRequest, id=job_request_id)
    assigned_candidates = job_request.candidates.all()
    
    # Get applications and their status
    incubation_job = IncubationJob.objects.filter(
        position=job_request.position_name,
        organization=job_request.organization
    ).first()
    
    candidate_status = {}
    if incubation_job:
        applications = Application.objects.filter(
            job=incubation_job,
            candidate__in=assigned_candidates
        ).select_related('candidate')
        
        for app in applications:
            candidate_status[app.candidate.id] = app.status

    context = {
        'job_request': job_request,
        'assigned_candidates': assigned_candidates,
        'candidate_status': candidate_status
    }
    return render(request, 'view_assigned_candidates.html', context)


