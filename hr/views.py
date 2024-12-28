from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from authentication.models import UserType
from jobrequest.models import JobRequest


@login_required
def get_profile(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'hr_profile.html', {'user': request.user, "user_type":user_type.user_type})

def evaluate_job_request(request, job_request_id):
    job_request = JobRequest.objects.get(id=job_request_id)
    job_request.request_status_hr = "HR-Approved"
    job_request.save()
    job_request.request_status_hr = "HR-Rejected"
    job_request.save()
    job_request.request_status_hr = "HR-Suspended"
    job_request.save()