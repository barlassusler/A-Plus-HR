from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from authentication.models import UserType
from jobrequest.models import JobRequest



# Create your views here.
@login_required
def dashboard(request):
    user_type = UserType.objects.filter(user=request.user).first()

    return render(request, 'director_dashboard.html',{'user': request.user, "user_type":user_type.user_type})

@login_required
def get_profile(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'director_profile.html', {'user': request.user, "user_type":user_type.user_type})