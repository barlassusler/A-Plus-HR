import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from authentication.models import UserType
from biko_hr.models import Interview, Application, Notification, InterviewAttributes
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


@login_required
def dashboard(request):
    user_type = UserType.objects.filter(user=request.user).first()
    applications = Application.objects.filter(assigned_by=request.user).order_by('-status')

    return render(request, 'hr_dashboard.html',{'user': request.user, "user_type":user_type.user_type, "applications":applications})


@login_required
def interview_assessment(request, interview_id):
    interview = get_object_or_404(
        Interview.objects.select_related(
            'candidate',
            'application__job__position',
            'evaluator'
        ),
        id=interview_id
    )
    
    # Check if the user is the assigned evaluator
    if interview.evaluator != request.user:
        messages.error(request, "You are not authorized to assess this interview.")
        return redirect('home')
    
    if request.method == 'POST':
        # Create InterviewAttributes with new fields
        attributes = InterviewAttributes.objects.create(
            candidate=interview.candidate,
            application=interview.application,
            problem_solving=request.POST.get('problem_solving'),
            technical_qualification=request.POST.get('technical_qualification'),
            Behaviour=request.POST.get('Behaviour'),
            Appearance=request.POST.get('Appearance'),
            Communucation=request.POST.get('Communucation'),
            Dedication_to_job=request.POST.get('Dedication_to_job'),
            Team_work=request.POST.get('Team_work'),
            Succes=request.POST.get('Succes'),
            open_to_improvement=request.POST.get('open_to_improvement'),
            advancement=request.POST.get('advancement'),
            leadership=request.POST.get('leadership'),
            Explanation=request.POST.get('Explanation'),
            HR_evaluation=request.POST.get('HR_evaluation'),
            manager_evaluation=request.POST.get('manager_evaluation')
        )
        
        # Update Interview
        interview.attributes_id = str(attributes.id)
        interview.general_assessment = request.POST.get('general_assessment')
        interview.work_hours_assessment = request.POST.get('work_hours_assessment')
        interview.decision = request.POST.get('decision')
        
        # Calculate and store evaluation scores (updated to include all evaluation fields)
        scores = {
            'problem_solving': request.POST.get('problem_solving'),
            'technical_qualification': request.POST.get('technical_qualification'),
            'Behaviour': request.POST.get('Behaviour'),
            'Appearance': request.POST.get('Appearance'),
            'Communucation': request.POST.get('Communucation'),
            'Dedication_to_job': request.POST.get('Dedication_to_job'),
            'Team_work': request.POST.get('Team_work'),
            'Succes': request.POST.get('Succes'),
            'open_to_improvement': request.POST.get('open_to_improvement'),
            'advancement': request.POST.get('advancement'),
            'leadership': request.POST.get('leadership'),
        }
        interview.evaluation_scores = json.dumps(scores)
        
        interview.save()
        
        # Update application status based on decision (adjust for new Decision_CHOICES)
        if interview.decision == 'Olumlu':
            interview.application.status = 'HR Assessment'
        elif interview.decision == 'Olumsuz':
            interview.application.status = 'Rejected'
        elif interview.decision == 'Beklemede':
            interview.application.status = 'Pending'
        interview.application.save()
        
        # Notify HR manager
        Notification.objects.create(
            user=interview.manager,
            message=f'Interview assessment completed for {interview.candidate.name} {interview.candidate.surname}',
            status='Unread'
        )
        
        messages.success(request, 'Interview assessment submitted successfully')
        return redirect('candidate_profile', candidate_id=interview.candidate.id)
    
    return render(request, 'interview_form.html', {
        'interview': interview,
        'evaluation_choices': InterviewAttributes.EVALUATION_CHOICES,  # Pass choices to template
        'decision_choices': InterviewAttributes.Decision_CHOICES,
    })

@login_required
def my_interviews(request):
    # Get pending interviews for the logged-in user
    pending_interviews = Interview.objects.filter(
        evaluator=request.user,
        decision='Pending'
    ).select_related(
        'candidate',
        'application__job__position'
    ).order_by('date')
    
    # Get completed interviews
    completed_interviews = Interview.objects.filter(
        evaluator=request.user
    ).exclude(
        decision='Pending'
    ).select_related(
        'candidate',
        'application__job__position'
    ).order_by('-date')
    
    return render(request, 'my_interviews.html', {
        'pending_interviews': pending_interviews,
        'completed_interviews': completed_interviews
    })