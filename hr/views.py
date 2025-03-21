import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
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
    # Get pending interviews for the logged-in user
    pending_interviews = Interview.objects.filter(
        evaluator=request.user,
        decision='Pending'
    ).select_related(
        'candidate',
        'application__job__position'
    ).order_by('date')
    return render(request, 'hr_dashboard.html',{'user': request.user, "user_type":user_type.user_type, "applications":applications, "pending_interviews":pending_interviews})


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
            interview=interview,
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
        'working_hour_choices': InterviewAttributes.WORKING_HOUR_CHOICES, 
    })

@login_required
def my_interviews(request):
    user_type = UserType.objects.filter(user=request.user).first()

    # Arama parametresini al
    search_query = request.GET.get('q', '')

    # Bekleyen görüşmeler
    pending_interviews = Interview.objects.filter(
        evaluator=request.user,
        decision='Pending'
    ).select_related(
        'candidate',
        'application__job__position'
    )
    if search_query:
        pending_interviews = pending_interviews.filter(
            Q(candidate__name__icontains=search_query) |
            Q(candidate__surname__icontains=search_query) |
            Q(application__job__position__position__icontains=search_query)
        )
    pending_interviews = pending_interviews.order_by('date')

    # Tamamlanmış görüşmeler
    completed_interviews = Interview.objects.filter(
        evaluator=request.user
    ).exclude(
        decision='Pending'
    ).select_related(
        'candidate',
        'application__job__position'
    )
    if search_query:
        completed_interviews = completed_interviews.filter(
            Q(candidate__name__icontains=search_query) |
            Q(candidate__surname__icontains=search_query) |
            Q(application__job__position__position__icontains=search_query)
        )
    completed_interviews = completed_interviews.order_by('-date')

    # Sayfalama: Her sayfada 10 görüşme
    page_number = request.GET.get('page', 1)  # URL'den sayfa numarasını al (varsayılan 1)
    
    # Bekleyen görüşmeler için sayfalama
    pending_paginator = Paginator(pending_interviews, 10)  # 10 görüşme per sayfa
    pending_page_obj = pending_paginator.get_page(page_number)

    # Tamamlanmış görüşmeler için sayfalama
    completed_paginator = Paginator(completed_interviews, 10)
    completed_page_obj = completed_paginator.get_page(page_number)

    return render(request, 'my_interviews.html', {
        'pending_interviews': pending_page_obj,  # Sayfalanmış nesne
        'completed_interviews': completed_page_obj,  # Sayfalanmış nesne
        'user': request.user,
        'user_type': user_type.user_type if user_type else None,
        'search_query': search_query  # Arama sorgusunu şablona geç
    })


@login_required
def completed_interview_detail(request, interview_id):
    # Interview nesnesini al
    interview = get_object_or_404(Interview, id=interview_id, evaluator=request.user)
    
    # İlgili InterviewAttributes nesnesini al (varsa)
    try:
        attributes = InterviewAttributes.objects.filter(interview=interview).order_by('-id').first()
    except InterviewAttributes.DoesNotExist:
        attributes = None

    context = {
        'interview': interview,
        'attributes': attributes,
    }
    return render(request, 'completed_interview_detail.html', context)