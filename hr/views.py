from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from authentication.models import UserType

@login_required
def get_profile(request):
    user_type = UserType.objects.filter(user=request.user).first()


    return render(request, 'hr_profile.html', {'user': request.user, "user_type":user_type.user_type})
