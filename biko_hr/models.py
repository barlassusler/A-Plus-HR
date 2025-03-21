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

class JobCategory(models.Model):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name
    
class Position(models.Model):
    position = models.CharField(max_length=100)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True,blank=True, default=None)

    def __str__(self):
        return self.position

# class Job(models.Model):
#     task = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.task


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15) ##TODO: Make this unique=True for production.
    experience = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    birth_date = models.DateField()
    residence_city = models.CharField(max_length=100)
    residence_district = models.CharField(max_length=100)
    education_level = models.CharField(max_length=50)        #choices=[
    #         ('read_write', 'Okuma Yazma Belgesi'),
    #         ('primary', 'İlkokul'),
    #         ('middle', 'Ortaokul'),
    #         ('high', 'Lise'),
    #         ('university', 'Üniversite'),
    #         ('postgraduate', 'Yüksek Lisans ve Üzeri'),
    #     ]
    # )
    school_name = models.CharField(max_length=150, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    desired_locations = models.ManyToManyField('Location', null=True, blank=True)

class IncubationJob(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=None,blank=True, null=True)
    category = models.OneToOneField(JobCategory, on_delete=models.CASCADE,  null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None,blank=True, null=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    status = models.CharField(max_length=50)
    preferred_locations = models.TextField()
    department = models.CharField(max_length=100)

class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(IncubationJob, on_delete=models.CASCADE) # in order to terminate or success the application after incubation period. Also shows the applied job.
    application_date = models.DateField()
    status = models.CharField(max_length=50, default="Pending")
    uploaded_resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateTimeField()  # Changed from DateField to DateTimeField
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
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    APPLICATION_SOURCE_TYPE_CHOICES = [
        ('Acıbadem Kariyer', 'Acıbadem Kariyer'),
        ('Secret CV	', 'Secret CV'),
        ('Kariyer Net', 'Kariyer Net'),
        ('İlave Kadro', 'İlave Kadro'),
        ('Yenibiriş.com', 'Yenibiriş.com'),
        (' Referans', ' Referans'),
    ]
    
    EVALUATION_CHOICES = [
        ('Zayıf', 'Zayıf'),
        ('Gelişmesi Gerekli', 'Gelişmesi Gerekli'),
        ('Beklentileri Karşılıyor', 'Beklentileri Karşılıyor'),
        ('Başarılı', 'Başarılı'),
        ('Çok Başarılı', 'Çok Başarılı'),
        
    ]
    WORKING_HOUR_CHOICES = [
        ('Esnek çalışma saatlerine uyum', 'Esnek çalışma saatlerine uyum'),
        ('Vardiyalı çalışmaya uyum', 'Vardiyalı çalışmaya uyum'),
        ('Hafta sonu çalışma günlerine uyum', 'Hafta sonu çalışma günlerine uyum'),
        
        
    ]
    
    Decision_CHOICES = [
        ('Olumlu', 'Olumlu'),
        ('Olumsuz ', 'Olumsuz'),
        ('Beklemede', 'Beklemede'),
        ('Farklı bir kadroda değerlendirilebilir', 'Farklı bir kadroda değerlendirilebilir'),
        
        
    ]
    Explanation=models.CharField(max_length=350,null=True)
    HR_evaluation=models.CharField(max_length=1000,blank=True, null=True)
    manager_evaluation=models.CharField(max_length=1000,blank=True, null=True)
    Behaviour=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    Appearance=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    Communucation=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    Dedication_to_job=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    Team_work=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    Succes=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    open_to_improvement=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    advancement=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    leadership=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    problem_solving=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)
    technical_qualification=models.CharField(max_length=100, choices=EVALUATION_CHOICES,blank=True, null=True)

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
    desired_position = models.CharField(max_length=100,default='Not specified')
    reference_outcome = models.CharField(max_length=100,default='Not specified')
    date = models.DateField(null=True)
    info_retriever_name = models.CharField(max_length=100,default='Not specified')
    referance_name = models.CharField(max_length=100,default='Not specified')  # Note: consider renaming to "reference_name" for consistency
    reference_phone = models.CharField(max_length=15,default='Not specified')
    reference_company = models.CharField(max_length=15,default='Not specified')
    reference_title = models.CharField(max_length=15,default='Not specified')
    refereance_relation_to_candidate = models.CharField(max_length=30)  # Note: consider "reference_relation_to_candidate"
    work_duration_with_company = models.TextField(default='Not specified')  # Added default
    work_duration_with_referee = models.TextField(default='Not specified')  # Added default
    duties = models.TextField(default='Not specified')  # Added default
    advancements = models.TextField(default='Not specified')  # Added default to fix the error
    dicipline = models.TextField(default='Not specified')  # Added default (should be "discipline")
    strengths = models.TextField(default='Not specified')  # Added default
    areas_for_improvement = models.TextField(default='Not specified')  # Added default
    major_error = models.TextField(default='Not specified')  # Added default
    responsibility = models.TextField(default='Not specified')  # Added default
    reason_for_leaving = models.TextField(default='Not specified')  # Added default
    would_work_again = models.TextField(default='Not specified')  # Added default
    further_explanation = models.TextField(default='Not specified')  # Added default

    class Meta:
        verbose_name = "Reference"
        verbose_name_plural = "References"

    def __str__(self):
        return f"Reference for {self.candidate} by {self.referance_name}"



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
