from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from authentication.forms import SignUpForm, LoginForm
# from authentication.models import CustomUser
from authentication.models import UserType

# def auth_index(request):
#     return render(request, "authentication/log_in.html")
from django.contrib.auth.models import User


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Map email to username
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                username = None
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Check the user profile for redirection based on user_type
                if request.user.is_authenticated:
                    usertype = UserType.objects.filter(user=user).first()  # Add parentheses to call .first()
                    if usertype:
                        if usertype.user_type == 'hr_staff':
                            return redirect('hr_dashboard')
                        elif usertype.user_type == 'organization_staff':
                            return redirect('organization_dashboard')
                        elif usertype.user_type == 'Director':
                            return redirect('director_dashboard')

                    else:
                        return render(request, 'log_in.html', {'form': form, 'message': 'Profile not found.'})
                # Authentication failed
                return render(request, 'log_in.html', {'form': form, 'message': 'Wrong credentials.'})
    else:
        form = LoginForm()

    # For GET requests, render the login form
    return render(request, 'log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('welcome')


@transaction.atomic
def sign_up(request): ## TODO: make email verification code in order to find out it is a real user, not a scammer.
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user_type = form.cleaned_data['user_type']

                # Create the User instance
                user = User.objects.create_user(username= username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                # Create the UserProfile instance
                user_type_object = UserType.objects.create(user=user, user_type=user_type)

                # Log the user in
                login(request, user)

                # Redirect to the user dashboard
                usertype = UserType.objects.filter(user=user).first()  # Add parentheses to call .first()
                if usertype:
                    if usertype.user_type == 'hr_staff':
                        return redirect('home')
                    elif usertype.user_type == 'organization_staff':
                        return redirect('organization_dashboard')
            except Exception as e:
                # Rollback the transaction if an error occurs
                transaction.set_rollback(True)
                print(f"An error occurred during sign-up: {e}")
                return render(request, 'sign_up.html',
                              {'form': form, 'message': 'An error occurred during sign-up. Please try again.'})
        else:
            # If form is invalid
            return render(request, 'sign_up.html',
                          {'form': form, 'message': 'Invalid form submission.'})
    else:
        form = SignUpForm()

    # For GET requests
    return render(request, 'sign_up.html', {'form': form})

from django.shortcuts import render, redirect

from django.db import transaction

def is_staff(user):
    return user.is_staff

def user_type(user):
    return user.is_staff

