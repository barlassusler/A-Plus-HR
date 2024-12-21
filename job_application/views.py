from django.shortcuts import render, get_object_or_404, redirect
from .forms import JobApplicationForm
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, fields
from datetime import date
from biko_hr.models import Application
from biko_hr.models import Location, Position

def job_application_list(request):
    search_query = request.GET.get('q', '')
    city_filter = request.GET.get('city', '')
    district_filter = request.GET.get('district', '')
    sort_option = request.GET.get('sort_option', 'name_asc')

    # Başvuruları al
    applications = JobApplication.objects.all()

    # Filtreleme
    if search_query:
        applications = applications.filter(full_name__icontains=search_query)
    if city_filter:
        applications = applications.filter(residence_city__icontains=city_filter)
    if district_filter:
        applications = applications.filter(residence_district__icontains=district_filter)

    # Yaş hesapla
    applications = applications.annotate(
        age=ExpressionWrapper(date.today().year - F('birth_date__year'), output_field=fields.IntegerField())
    )

    # Sıralama
    if sort_option == "name_asc":
        applications = applications.order_by('full_name')
    elif sort_option == "name_desc":
        applications = applications.order_by('-full_name')
    elif sort_option == "age_asc":
        applications = applications.order_by('age')
    elif sort_option == "age_desc":
        applications = applications.order_by('-age')
    elif sort_option == "experience_asc":
        applications = applications.order_by('experience')
    elif sort_option == "experience_desc":
        applications = applications.order_by('-experience')

    # Sayfalama
    paginator = Paginator(applications, 10)  # Sayfa başına 10 başvuru
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render fonksiyonu ile şablonu ve veriyi döndür
    return render(request, 'job_application_list.html', {
        'candidates': page_obj,
        'search_query': search_query,
        'city_filter': city_filter,
        'district_filter': district_filter,
        'sort_option': sort_option,
    })

def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'application_detail.html', {'application': application})

def job_application_form(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_application_list')  # Başvurular listesine yönlendir
    else:
        form = JobApplicationForm()

    # `Position` ve `Location` verilerini formda göstermek için context'e ekleyin
    context = {
        'form': form,
        'positions': Position.objects.all(),
        'locations': Location.objects.all()
    }

    return render(request, 'job_application_form.html', context)




