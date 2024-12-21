from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from authentication.models import UserType

@login_required
def dashboard(request):
    user_type = UserType.objects.filter(user=request.user).first()

    return render(request, 'organization_dashboard.html',{'user': request.user, "user_type":user_type.user_type})

@login_required
def get_profile(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'organization_profile.html', {'user': request.user, "user_type":user_type.user_type})
