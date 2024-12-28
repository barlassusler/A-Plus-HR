from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from authentication.models import UserType
from jobrequest.models import JobRequest


@login_required
def dashboard(request):
    user_type = UserType.objects.filter(user=request.user).first()

    return render(request, 'organization_dashboard.html',{'user': request.user, "user_type":user_type.user_type})

@login_required
def get_profile(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'organization_profile.html', {'user': request.user, "user_type":user_type.user_type})

def evaluate_job_request(request, job_request_id):
    job_request = JobRequest.objects.get(id=job_request_id)
    job_request.request_status_hr = "Organization-Manager-Approved"
    job_request.save()
    job_request.request_status_hr = "Organization-Manager-Rejected"
    job_request.save()
    job_request.request_status_hr = "Organization-Manager-Suspended"
    job_request.save()