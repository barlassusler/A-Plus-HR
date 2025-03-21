from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.utils import timezone

from jobrequest.models import JobRequest
from .forms import ApplicationForm, CandidateForm
from django.db.models import F, ExpressionWrapper, fields
from datetime import date
from biko_hr.models import Application, Location, Position, Candidate, IncubationJob
from datetime import date
from django.db.models import F, ExpressionWrapper, IntegerField
from django.shortcuts import render
from biko_hr.models import Application

from django.core.paginator import Paginator
from django.shortcuts import render
from biko_hr.models import Application, Profile, Location
from datetime import date

def job_application_list(request):
    # Fetch filters from GET request
    search_query = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '').strip()
    district_filter = request.GET.get('district', '').strip()
    sort_option = request.GET.get('sort_option', 'name_asc')
    filter_type = request.GET.get('filter', 'general')  # Yeni: Filtre tipi

    # Fetch applications with related candidate data
    applications = Application.objects.select_related('candidate')

    # Kullanıcı lokasyonu
    user_profile = Profile.objects.filter(user=request.user).first()
    user_location = user_profile.Location if user_profile and user_profile.Location else None
    print(f"User: {request.user}, Profile: {user_profile}, Location: {user_location}")

    # Apply filters
    if search_query:
        applications = applications.filter(
            candidate__name__icontains=search_query
        ) | applications.filter(
            candidate__surname__icontains=search_query
        )
    if city_filter:
        applications = applications.filter(candidate__residence_city__icontains=city_filter)
    if district_filter:
        applications = applications.filter(candidate__residence_district__icontains=district_filter)

    # Kullanıcı lokasyonuna göre filtreleme
    if filter_type == 'user_location' and user_location:
        applications = applications.filter(candidate__residence_city=user_location.location)
        print(f"Filtering by location: {user_location.location}, Results: {applications.count()}")

    # Apply sorting
    if sort_option == "name_asc":
        applications = applications.order_by('candidate__name', 'candidate__surname')
    elif sort_option == "name_desc":
        applications = applications.order_by('-candidate__name', '-candidate__surname')
    elif sort_option == "age_asc":
        applications = applications.order_by('candidate__birth_date')  # Doğum tarihi artan
    elif sort_option == "age_desc":
        applications = applications.order_by('-candidate__birth_date')  # Doğum tarihi azalan

    # Yaş hesaplama (doğru yaş için)
    for application in applications:
        today = date.today()
        birth_date = application.candidate.birth_date
        application.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Sayfalama
    paginator = Paginator(applications, 10)  # 10 başvuru per sayfa
    page_number = request.GET.get('page')
    candidates = paginator.get_page(page_number)

    # Render template with context
    return render(request, 'job_application_list.html', {
        'applications': candidates,  # Sayfalanmış sonuçlar
        'search_query': search_query,
        'city_filter': city_filter,
        'district_filter': district_filter,
        'sort_option': sort_option,
        'candidates': candidates,  # Şablon sayfalama için
    })


def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'application_detail.html', {'application': application})


def job_application_form(request):

    if request.method == 'POST':
        # Formları oluşturuyoruz
        candidate_form = CandidateForm(request.POST)
        application_form = ApplicationForm(request.POST, request.FILES)
        print("POST Data:", request.POST)  # Debugging
        print("FILES Data:", request.FILES)  # Debugging
        if candidate_form.is_valid():
            pass
        else:
            print("Candidate Form Errors:", candidate_form.errors)  # Print errors here
            raise forms.ValidationError("Aday bilgileri geçersiz.")
        # Formlar geçerliyse işlemi yapıyoruz
        if candidate_form.is_valid() and application_form.is_valid():
            # Candidate modelini kaydediyoruz
            candidate = candidate_form.save(commit=False)  # Önce kaydetme işlemi durduruluyor
            candidate.save() # Adayı kaydediyoruz (ancak dönüş değerini değiştirmiyoruz!)
            print("Candidate saved:", candidate)  # Debugging için

            # Kullanıcının seçtiği birden fazla lokasyonu alıyoruz
            selected_location_ids = request.POST.getlist('desired_locations')
            if selected_location_ids:
                selected_locations = Location.objects.filter(id__in=selected_location_ids)
                candidate.desired_locations.set(selected_locations)  # ManyToMany ilişkilendirme
            else:
                # Handle the case when no location is selected (e.g., don't set anything or set default)
                candidate.desired_locations.clear()  # Clear existing locations if none are selected

            job_id = request.POST.get('application_job')
            print(f"Selected job ID: {job_id}")

            position = get_object_or_404(JobRequest, id=job_id)  # Ensure the JobRequest exists
            incubation_job = IncubationJob.objects.create(position=position.position_name)

            # Application modelini kaydediyoruz (commit=False çünkü ilişkilendirme yapmamız gerekiyor)
            application = application_form.save(commit=False)
            application.candidate = candidate  # Candidate ile ilişkilendiriyoruz
            application.job = incubation_job  # Associate the job with the application
            application.application_date = timezone.now()  # Başvuru tarihini kaydediyoruz
            application.save()  # Application kaydını yapıyoruz
            application_form.save_m2m()  # Many-to-many ilişkilerini kaydediyoruz

            # Başvuru başarılı, listeye yönlendiriyoruz
            return redirect('job_application_list')
        else:
            print(candidate_form.errors)  # To debug form validation errors
            print(application_form.errors)  # To debug form validation errors
        # Eğer formda hata varsa, formu tekrar render ediyoruz
        return render(request, 'job_application_form.html', {
            'candidate_form': candidate_form,
            'application_form': application_form,
            'positions': JobRequest.objects.all(),
            'locations': Location.objects.all(),
        })

    # GET isteği için boş formlar döndür
    candidate_form = CandidateForm()
    application_form = ApplicationForm()

    return render(request, 'job_application_form.html', {
        'candidate_form': CandidateForm(),
        'application_form': ApplicationForm(),
        'positions': JobRequest.objects.all(),
        'locations': Location.objects.all(),
    })


def success_page(request):
    return render(request, 'success_page.html')  # Başarı sayfasını render et
