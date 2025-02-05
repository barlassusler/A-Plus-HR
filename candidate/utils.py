from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta

def send_interview_notification(interview):
    # Send email to candidate
    candidate_subject = f'Interview Scheduled - {interview.application.job.position.position}'
    candidate_message = render_to_string('emails/interview_scheduled_candidate.html', {
        'interview': interview,
        'company_name': 'Your Company Name'
    })
    
    send_mail(
        candidate_subject,
        '',
        settings.EMAIL_HOST_USER,
        [interview.candidate.email],
        html_message=candidate_message,
        fail_silently=False,
    )
    
    # Send email to evaluator
    evaluator_subject = f'Interview Assignment - {interview.candidate.name} {interview.candidate.surname}'
    evaluator_message = render_to_string('emails/interview_scheduled_evaluator.html', {
        'interview': interview,
        'company_name': 'Your Company Name'
    })
    
    send_mail(
        evaluator_subject,
        '',
        settings.EMAIL_HOST_USER,
        [interview.evaluator.email],
        html_message=evaluator_message,
        fail_silently=False,
    )

def send_interview_reminder():
    """
    Send reminder emails for interviews scheduled in the next 24 hours
    This should be run by a scheduled task (e.g., using Django-crontab or Celery)
    """
    tomorrow = datetime.now().date() + timedelta(days=1)
    
    # Get interviews scheduled for tomorrow
    upcoming_interviews = Interview.objects.filter(
        date=tomorrow,
        decision='Pending'
    ).select_related('candidate', 'evaluator', 'application__job__position')
    
    for interview in upcoming_interviews:
        # Remind candidate
        candidate_subject = f'Interview Reminder - Tomorrow'
        candidate_message = render_to_string('emails/interview_reminder_candidate.html', {
            'interview': interview,
            'company_name': 'Your Company Name'
        })
        
        send_mail(
            candidate_subject,
            '',
            settings.EMAIL_HOST_USER,
            [interview.candidate.email],
            html_message=candidate_message,
            fail_silently=False,
        )
        
        # Remind evaluator
        evaluator_subject = f'Interview Reminder - {interview.candidate.name} {interview.candidate.surname}'
        evaluator_message = render_to_string('emails/interview_reminder_evaluator.html', {
            'interview': interview,
            'company_name': 'Your Company Name'
        })
        
        send_mail(
            evaluator_subject,
            '',
            settings.EMAIL_HOST_USER,
            [interview.evaluator.email],
            html_message=evaluator_message,
            fail_silently=False,
        ) 