from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from authentication.models import UserType

@login_required
def home(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'home.html', {'user': request.user, "user_type":user_type.user_type})


def get_welcome(request):
    return render(request, 'welcome.html')

from .models import Profile

# def profile_view(request):
#     return render(request, 'hr_profile.html', {'user': request.user})
