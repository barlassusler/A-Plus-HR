from django.shortcuts import render, get_object_or_404, redirect
from biko_hr.models import JobCategory, Application, Candidate, Position, Interview, Evaluation, IncubationJob, InterviewAttributes, IncubationEvaluation, Reference, IncubationAttributes
from jobrequest.models import JobRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
import json
from biko_hr.models import Notification
from .utils import send_interview_notification
from authentication.models import UserType


def get_candidate_pool(request):
    # Get raw categories for the dropdown
    raw_categories = JobCategory.objects.all()
    
    # Get categories with their related data for the cards
    categories = JobCategory.objects.prefetch_related(
        'position_set',
        'position_set__incubationjob_set__application_set__candidate'
    ).all()
    
    # Structure the data for the cards
    category_data = []
    for category in categories:
        applications = []
        for position in category.position_set.all():
            for job in position.incubationjob_set.all():
                for application in job.application_set.all():
                    applications.append({
                        'candidate': application.candidate,
                        'position': position.position,
                        'job': job,
                        'application_date': application.application_date,
                        'status': application.status
                    })
        
        category_data.append({
            'id': category.id,
            'name': category.category_name,
            'applications': applications
        })

    return render(request, 'candidate_pool_dashboard.html', {
        'raw_categories': raw_categories,  # For the dropdown
        'categories': category_data       # For the cards
    })


# def get_candidate_pool(request):
#     # Simulated example data
#     categories = [
#         {
#             "id": 1,
#             "category_name": "Operasyon ve Destek",
#             "persons": [
#                 {"name": "Alice Smith", "position": "Backend Developer", "office": "New York", "avatar_url": "avatars/alice.jpg"},
#                 {"name": "Bob Johnson", "position": "Frontend Developer", "office": "San Francisco", "avatar_url": "avatars/bob.jpg"},
#                 {"name": "Charlie Davis", "position": "Full-Stack Developer", "office": "Austin", "avatar_url": "avatars/charlie.jpg"},
#                 {"name": "Diana Lee", "position": "DevOps Engineer", "office": "Seattle", "avatar_url": "avatars/diana.jpg"},
#                 {"name": "Evan Garcia", "position": "QA Engineer", "office": "Boston", "avatar_url": "avatars/evan.jpg"},
#                 {"name": "Fiona Brown", "position": "Software Architect", "office": "Chicago", "avatar_url": "avatars/fiona.jpg"},
#                 {"name": "George White", "position": "Mobile Developer", "office": "Miami", "avatar_url": "avatars/george.jpg"},
#             ],
#         },
#         {
#             "id": 2,
#             "category_name": "Gıda ve Yemek Hizmetleri",
#             "persons": [
#                 {"name": "Hannah Green", "position": "Data Scientist", "office": "New York", "avatar_url": "avatars/hannah.jpg"},
#                 {"name": "Ian Black", "position": "Machine Learning Engineer", "office": "San Francisco", "avatar_url": "avatars/ian.jpg"},
#                 {"name": "Jack Brown", "position": "AI Researcher", "office": "Austin", "avatar_url": "avatars/jack.jpg"},
#                 {"name": "Karen Gray", "position": "Data Analyst", "office": "Seattle", "avatar_url": "avatars/karen.jpg"},
#                 {"name": "Liam Carter", "position": "Big Data Engineer", "office": "Boston", "avatar_url": "avatars/liam.jpg"},
#                 {"name": "Mia Lopez", "position": "Statistician", "office": "Chicago", "avatar_url": "avatars/mia.jpg"},
#                 {"name": "Nathan Scott", "position": "Data Engineer", "office": "Miami", "avatar_url": "avatars/nathan.jpg"},
#             ],
#         },
#         {
#             "id": 3,
#             "category_name": "Lojistik ve Depo",
#             "persons": [
#                 {"name": "Olivia Morgan", "position": "HR Specialist", "office": "New York", "avatar_url": "avatars/olivia.jpg"},
#                 {"name": "Paul Parker", "position": "Recruiter", "office": "San Francisco", "avatar_url": "avatars/paul.jpg"},
#                 {"name": "Quinn Walker", "position": "HR Manager", "office": "Austin", "avatar_url": "avatars/quinn.jpg"},
#                 {"name": "Rachel Hill", "position": "Talent Acquisition", "office": "Seattle", "avatar_url": "avatars/rachel.jpg"},
#                 {"name": "Samuel Young", "position": "Training Coordinator", "office": "Boston", "avatar_url": "avatars/samuel.jpg"},
#                 {"name": "Tina Bell", "position": "Compensation Analyst", "office": "Chicago", "avatar_url": "avatars/tina.jpg"},
#                 {"name": "Ursula King", "position": "HR Consultant", "office": "Miami", "avatar_url": "avatars/ursula.jpg"},
#             ],
#         },
#         {
#             "id": 4,
#             "category_name": "Kafe ve Servis Hizmetleri",
#             "persons": [
#                 {"name": "Olivia Morgan", "position": "HR Specialist", "office": "New York",
#                  "avatar_url": "avatars/olivia.jpg"},
#                 {"name": "Paul Parker", "position": "Recruiter", "office": "San Francisco",
#                  "avatar_url": "avatars/paul.jpg"},
#                 {"name": "Quinn Walker", "position": "HR Manager", "office": "Austin",
#                  "avatar_url": "avatars/quinn.jpg"},
#                 {"name": "Rachel Hill", "position": "Talent Acquisition", "office": "Seattle",
#                  "avatar_url": "avatars/rachel.jpg"},
#                 {"name": "Samuel Young", "position": "Training Coordinator", "office": "Boston",
#                  "avatar_url": "avatars/samuel.jpg"},
#                 {"name": "Tina Bell", "position": "Compensation Analyst", "office": "Chicago",
#                  "avatar_url": "avatars/tina.jpg"},
#                 {"name": "Ursula King", "position": "HR Consultant", "office": "Miami",
#                  "avatar_url": "avatars/ursula.jpg"},
#             ],
#         },
#     ]
#
#     return render(request, "candidate_pool_dashboard.html", {"category": categories})


@login_required
def candidate_profile(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    hr_staff = User.objects.filter(user_type__user_type='hr_staff').exclude(user_type__isnull=True)
    managers = User.objects.filter(user_type__user_type__in=['organization_staff', 'Director']).exclude(user_type__isnull=True)
    applications = Application.objects.filter(candidate=candidate)
    evaluations = Evaluation.objects.filter(candidate=candidate)
    interviews = Interview.objects.filter(candidate=candidate)
    job_requests = JobRequest.objects.all()  # Açık işler için uygun bir filtre ekleyin

    context = {
        'candidate': candidate,
        'applications': applications,
        'evaluations': evaluations,
        'interviews': interviews,
        'hr_staff': hr_staff,
        'managers': managers,
        'job_requests': job_requests,
    }
    
    return render(request, 'candidate_profile.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(JobCategory, id=category_id)
    
    # Get all applications for this category
    applications = []
    for position in category.position_set.all():
        for job in position.incubationjob_set.all():
            for application in job.application_set.all():
                applications.append({
                    'candidate': application.candidate,
                    'position': position.position,
                    'job': job,
                    'application_date': application.application_date,
                    'status': application.status
                })
    
    # Add pagination
    paginator = Paginator(applications, 20)  # Show 20 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'candidate_category_detail.html', {
        'category': category,
        'page_obj': page_obj,
    })



@login_required
def assign_job(request, candidate_id):
    if request.method == 'POST':
        job_request = get_object_or_404(JobRequest, id=request.POST['job_request'])
        
        # Create or get IncubationJob
        incubation_job, created = IncubationJob.objects.get_or_create(
            position=job_request.position_name,
            organization=job_request.organization,
            defaults={
                'title': f"{job_request.position_name} at {job_request.organization}",
                'description': job_request.description or '',
                'required_skills': job_request.special_requirements or '',
                'status': 'Active',
                'preferred_locations': job_request.location.location if job_request.location else '',
                'department': job_request.organization.organization
            }
        )
        
        # Create application
        application = Application.objects.create(
            candidate_id=candidate_id,
            job=incubation_job,
            application_date=date.today(),
            status='Pending',
            assigned_by=request.user
        )
        
        if 'resume' in request.FILES:
            application.uploaded_resume = request.FILES['resume']
            application.save()
        
        messages.success(request, 'Candidate assigned to job successfully')
    return redirect('candidate_profile', candidate_id=candidate_id)


@login_required
def add_hr_note(request, candidate_id):
    if request.method == 'POST':
        Interview.objects.create(
            candidate_id=candidate_id,
            application=None,  # No specific application for general notes
            date=date.today(),
            general_assessment=request.POST['content'],
            manager=request.user,  # Author of the note
            evaluator=request.user,  # Same as manager for HR notes
            evaluator_role='HR Note',
            application_source='Internal Note',
            work_hours_assessment='',
            evaluation_scores='',
            decision='Note'  # Indicates this is a note, not an interview
        )
        messages.success(request, 'Note added successfully')
    return redirect('candidate_profile', candidate_id=candidate_id)


@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    candidate = application.candidate

    # Get all HR staff users
    hr_staff = User.objects.filter(
        user_type__user_type='hr_staff'
    ).exclude(
        user_type__isnull=True
    )

    # Get all managers (organization staff and directors)
    managers = User.objects.filter(
        user_type__user_type__in=['organization_staff', 'Director']
    ).exclude(
        user_type__isnull=True
    )

    if request.method == 'POST':
        try:
            # Combine date and time
            interview_date = request.POST.get('date')
            interview_time = request.POST.get('time')
            interview_datetime = datetime.strptime(f"{interview_date} {interview_time}", "%Y-%m-%d %H:%M")

            # Create interview with datetime
            interview = Interview.objects.create(
                application=application,
                date=interview_datetime,  # Now storing the full datetime
                candidate=candidate,
                evaluator=get_object_or_404(User, id=request.POST.get('evaluator')),
                evaluator_role=request.POST.get('evaluator_role'),
                application_source=request.POST.get('application_source'),
                manager=get_object_or_404(User, id=request.POST.get('manager')),
                general_assessment='',
                work_hours_assessment='',
                evaluation_scores='',
                decision='Pending'
            )

            messages.success(request, 'Interview scheduled successfully')
            return redirect('candidate_profile', candidate_id=candidate.id)

        except Exception as e:
            messages.error(request, f'Error scheduling interview: {str(e)}')

    context = {
        'candidate': candidate,
        'application': application,
        'hr_staff': hr_staff,
        'managers': managers,
    }
    return render(request, 'schedule_interview.html', context)


## CANDIDATE EVALUATION
@login_required
def candidate_evaluation(request, application_id):
    application = get_object_or_404(
        Application.objects.select_related(
            'candidate', 
            'job'
        ),
        id=application_id
    )
    
    # Get all interviews for this application
    interviews = Interview.objects.filter(
        application=application
    ).select_related('evaluator')
    
    if request.method == 'POST':
        # Calculate average scores from interviews
        interview_scores = []
        for interview in interviews:
            if interview.evaluation_scores:
                scores = json.loads(interview.evaluation_scores)
                interview_scores.append({
                    'problem_solving': int(scores.get('problem_solving', 0)),
                    'technical_skills': int(scores.get('technical_skills', 0))
                })
        
        avg_problem_solving = sum(s['problem_solving'] for s in interview_scores) / len(interview_scores)
        avg_technical_skills = sum(s['technical_skills'] for s in interview_scores) / len(interview_scores)
        
        # Create final evaluation
        evaluation = Evaluation.objects.create(
            candidate=application.candidate,
            job=application.job,
            interview_decision=request.POST.get('decision'),
            evaluation_scores=json.dumps({
                'avg_problem_solving': avg_problem_solving,
                'avg_technical_skills': avg_technical_skills
            }),
            evaluator=request.user,
            decision=request.POST.get('decision')
        )
        
        # If approved, create incubation period
        if request.POST.get('decision') == 'Approved':
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            IncubationEvaluation.objects.create(
                candidate=application.candidate,
                job=application.job,
                start_date=start_date,
                end_date=start_date + timedelta(days=90),  # 3 months
                evaluator=request.user,
                manager_decision='Pending'
            )
            application.status = 'Incubation'
        else:
            application.status = 'Rejected'
        
        application.save()
        messages.success(request, 'Evaluation completed successfully')
        return redirect('candidate_profile', candidate_id=application.candidate.id)
    
    return render(request, 'evaluation_form.html', {
        'application': application,
        'interviews': interviews
    })

@login_required
def incubation_evaluation(request, incubation_id):
    incubation = get_object_or_404(
        IncubationEvaluation.objects.select_related(
            'candidate',
            'job'
        ),
        id=incubation_id
    )
    
    if request.method == 'POST':
        # Create incubation attributes
        attributes = IncubationAttributes.objects.create(
            candidate=incubation.candidate,
            team_work=request.POST.get('team_work'),
            rule_compliance=request.POST.get('rule_compliance'),
            learning_capacity=request.POST.get('learning_capacity'),
            willingness_to_learn=request.POST.get('willingness_to_learn'),
            stress_handling=request.POST.get('stress_handling'),
            tool_usage=request.POST.get('tool_usage'),
            task_completion=request.POST.get('task_completion'),
            interpersonal_skills=request.POST.get('interpersonal_skills'),
            leadership=request.POST.get('leadership'),
            planning=request.POST.get('planning'),
            problem_solving=request.POST.get('problem_solving')
        )
        
        # Update incubation evaluation
        incubation.incubation_attributes_id = str(attributes.id)
        incubation.evaluation_scores = json.dumps({
            'team_work': attributes.team_work,
            'rule_compliance': attributes.rule_compliance,
            'learning_capacity': attributes.learning_capacity,
            'willingness_to_learn': attributes.willingness_to_learn,
            'stress_handling': attributes.stress_handling,
            'tool_usage': attributes.tool_usage,
            'task_completion': attributes.task_completion,
            'interpersonal_skills': attributes.interpersonal_skills,
            'leadership': attributes.leadership,
            'planning': attributes.planning,
            'problem_solving': attributes.problem_solving
        })
        incubation.manager_decision = request.POST.get('decision')
        incubation.decision_explanation = request.POST.get('explanation')
        incubation.save()
        
        # Update application status
        application = Application.objects.get(
            candidate=incubation.candidate,
            job=incubation.job
        )
        application.status = 'Completed' if request.POST.get('decision') == 'Approved' else 'Rejected'
        application.save()
        
        messages.success(request, 'Incubation evaluation completed successfully')
        return redirect('candidate_profile', candidate_id=incubation.candidate.id)
    
    return render(request, 'incubation_evaluation_form.html', {
        'incubation': incubation
    })

@login_required
def add_reference(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        try:
            Reference.objects.create(
                candidate=candidate,
                desired_position=request.POST.get('desired_position'),
                reference_outcome=request.POST.get('reference_outcome'),
                date=request.POST.get('date'),
                info_retriever_name=request.POST.get('info_retriever_name'),
                reference_name=request.POST.get('reference_name'),
                reference_phone=request.POST.get('reference_phone'),
                reference_company=request.POST.get('reference_company'),
                reference_title=request.POST.get('reference_title'),
                refereance_relation_to_candidate=request.POST.get('refereance_relation_to_candidate'),
                work_duration_with_company=request.POST.get('work_duration_with_company'),
                work_duration_with_referee=request.POST.get('work_duration_with_referee'),
                duties=request.POST.get('duties'),
                advancements=request.POST.get('advancements'),
                dicipline=request.POST.get('dicipline'),
                strengths=request.POST.get('strengths'),
                areas_for_improvement=request.POST.get('areas_for_improvement'),
                major_error=request.POST.get('major_error'),
                responsibility=request.POST.get('responsibility'),
                reason_for_leaving=request.POST.get('reason_for_leaving'),
                would_work_again=request.POST.get('would_work_again'),
                further_explanation=request.POST.get('further_explanation')
            )
            messages.success(request, 'Reference added successfully')
            return redirect('candidate_profile', candidate_id=candidate_id)
        except Exception as e:
            messages.error(request, f'Error adding reference: {str(e)}')
    
    return render(request, 'add_reference.html', {
        'candidate': candidate
    })