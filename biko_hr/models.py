from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location

class Organization(models.Model):
    organization = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization

class Position(models.Model):
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position

class Job(models.Model):
    task = models.CharField(max_length=100)

    def __str__(self):
        return self.task


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    experience = models.TextField()
    skills = models.TextField()
    birth_date = models.DateField()
    residence_city = models.CharField(max_length=100)
    residence_district = models.CharField(max_length=100)
    education_level = models.CharField(max_length=50)
    school_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)

class IncubationJob(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    status = models.CharField(max_length=50)
    preferred_locations = models.TextField()
    department = models.CharField(max_length=100)

class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(IncubationJob, on_delete=models.CASCADE)
    application_date = models.DateField()
    status = models.CharField(max_length=50)
    uploaded_resume = models.FileField(upload_to='resumes/')

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateField()
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    application_source = models.CharField(max_length=200)
    general_assessment = models.TextField()
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluated_interviews')
    evaluator_role = models.CharField(max_length=100)
    attributes_id = models.TextField()  # Placeholder for complex attributes
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_interviews')
    work_hours_assessment = models.TextField()
    evaluation_scores = models.TextField()
    decision = models.TextField()



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)


class Evaluation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(IncubationJob, on_delete=models.CASCADE)
    interview_decision = models.TextField() ## TODO: InterviewDecisionId? Or Interviews or Sum Interview scores decide
    evaluation_scores = models.TextField()
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.TextField()




class InterviewAttributes(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    problem_solving = models.IntegerField()
    technical_skills = models.IntegerField()
    # Add other attributes as needed

class IncubationEvaluation(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(IncubationJob, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    incubation_attributes_id = models.TextField()
    evaluation_scores = models.TextField()
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    manager_decision = models.TextField()
    decision_explanation = models.TextField()

class IncubationAttributes(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    team_work = models.IntegerField()
    rule_compliance = models.IntegerField()
    learning_capacity = models.IntegerField()
    willingness_to_learn = models.IntegerField()
    stress_handling = models.IntegerField()
    tool_usage = models.IntegerField()
    task_completion = models.IntegerField()
    interpersonal_skills = models.IntegerField()
    leadership = models.IntegerField()
    planning = models.IntegerField()
    problem_solving = models.IntegerField()

class Reference(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    reference_name = models.CharField(max_length=100)
    reference_role = models.CharField(max_length=100)
    reference_company = models.CharField(max_length=100)
    reference_phone = models.CharField(max_length=15)
    work_duration = models.TextField()
    duties = models.TextField()
    strengths = models.TextField()
    weaknesses = models.TextField()
    reason_for_leaving = models.TextField()
    would_work_again = models.BooleanField()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    Position=models.ForeignKey(Position,on_delete=models.CASCADE,blank=True, null=True)
    Location=models.ForeignKey(Location,on_delete=models.CASCADE,blank=True, null=True)
    Organization=models.ForeignKey(Organization,on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
     if self.user:
        return self.user.username
     return "No user assigned"
