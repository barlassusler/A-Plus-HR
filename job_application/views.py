from django.shortcuts import render, get_object_or_404, redirect
from .forms import ApplicationForm, CandidateForm
from django.db.models import F, ExpressionWrapper, fields
from datetime import date
from .models import Application, Location, Position, Candidate

def job_application_list(request):
    search_query = request.GET.get('q', '')
    city_filter = request.GET.get('city', '')
    district_filter = request.GET.get('district', '')
    sort_option = request.GET.get('sort_option', 'name_asc')

    # Başvuruları getir
    applications = Application.objects.select_related('candidate')

    # Filtreleme
    if search_query:
        applications = applications.filter(candidate__full_name__icontains=search_query)
    if city_filter:
        applications = applications.filter(candidate__residence_city__icontains=city_filter)
    if district_filter:
        applications = applications.filter(candidate__residence_district__icontains=district_filter)

    # Yaş hesapla
    applications = applications.annotate(
        age=ExpressionWrapper(
            date.today().year - F('candidate__birth_date__year'),
            output_field=fields.IntegerField()
        )
    )

    # Sıralama
    if sort_option == "name_asc":
        applications = applications.order_by('candidate__full_name')
    elif sort_option == "name_desc":
        applications = applications.order_by('-candidate__full_name')
    elif sort_option == "age_asc":
        applications = applications.order_by('age')
    elif sort_option == "age_desc":
        applications = applications.order_by('-age')

    # Template'e gönderilecek veriler
    return render(request, 'job_application_list.html', {
        'applications': applications,
        'search_query': search_query,
        'city_filter': city_filter,
        'district_filter': district_filter,
        'sort_option': sort_option,
    })


def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'application_detail.html', {'application': application})


def job_application_form(request):
    if request.method == 'POST':
        # Formları oluşturuyoruz
        candidate_form = CandidateForm(request.POST)
        application_form = ApplicationForm(request.POST, request.FILES)

        # Formlar geçerliyse işlemi yapıyoruz
        if candidate_form.is_valid() and application_form.is_valid():
            # Candidate modelini kaydediyoruz
            candidate = candidate_form.save()

            # Application modelini kaydediyoruz (commit=False çünkü ilişkilendirme yapmamız gerekiyor)
            application = application_form.save(commit=False)
            application.candidate = candidate  # Candidate ile ilişkilendiriyoruz
            application.save()  # Application kaydını yapıyoruz
            application_form.save_m2m()  # Many-to-many ilişkilerini kaydediyoruz

            # Başvuru başarılı, listeye yönlendiriyoruz
            return redirect('job_application_list')

        # Eğer formda hata varsa, formu tekrar render ediyoruz
        return render(request, 'job_application_form.html', {
            'candidate_form': candidate_form,
            'application_form': application_form,
            'positions': Position.objects.all(),
            'locations': Location.objects.all(),
        })

    # GET isteği için boş formlar döndür
    candidate_form = CandidateForm()
    application_form = ApplicationForm()

    return render(request, 'job_application_form.html', {
        'candidate_form': candidate_form,
        'application_form': application_form,
        'positions': Position.objects.all(),
        'locations': Location.objects.all(),
    })


def success_page(request):
    return render(request, 'success_page.html')  # Başarı sayfasını render et
