from django.shortcuts import render

# Create your views here.
from biko_hr.models import JobCategory


def get_candidate_pool(request):
    category = JobCategory.objects.all()

    return render(request, 'candidate_pool_dashboard.html', {"category":category})
from django.shortcuts import render

def get_candidate_pool(request):
    # Simulated example data
    categories = [
        {
            "id": 1,
            "category_name": "Operasyon ve Destek",
            "persons": [
                {"name": "Alice Smith", "position": "Backend Developer", "office": "New York", "avatar_url": "avatars/alice.jpg"},
                {"name": "Bob Johnson", "position": "Frontend Developer", "office": "San Francisco", "avatar_url": "avatars/bob.jpg"},
                {"name": "Charlie Davis", "position": "Full-Stack Developer", "office": "Austin", "avatar_url": "avatars/charlie.jpg"},
                {"name": "Diana Lee", "position": "DevOps Engineer", "office": "Seattle", "avatar_url": "avatars/diana.jpg"},
                {"name": "Evan Garcia", "position": "QA Engineer", "office": "Boston", "avatar_url": "avatars/evan.jpg"},
                {"name": "Fiona Brown", "position": "Software Architect", "office": "Chicago", "avatar_url": "avatars/fiona.jpg"},
                {"name": "George White", "position": "Mobile Developer", "office": "Miami", "avatar_url": "avatars/george.jpg"},
            ],
        },
        {
            "id": 2,
            "category_name": "Gıda ve Yemek Hizmetleri",
            "persons": [
                {"name": "Hannah Green", "position": "Data Scientist", "office": "New York", "avatar_url": "avatars/hannah.jpg"},
                {"name": "Ian Black", "position": "Machine Learning Engineer", "office": "San Francisco", "avatar_url": "avatars/ian.jpg"},
                {"name": "Jack Brown", "position": "AI Researcher", "office": "Austin", "avatar_url": "avatars/jack.jpg"},
                {"name": "Karen Gray", "position": "Data Analyst", "office": "Seattle", "avatar_url": "avatars/karen.jpg"},
                {"name": "Liam Carter", "position": "Big Data Engineer", "office": "Boston", "avatar_url": "avatars/liam.jpg"},
                {"name": "Mia Lopez", "position": "Statistician", "office": "Chicago", "avatar_url": "avatars/mia.jpg"},
                {"name": "Nathan Scott", "position": "Data Engineer", "office": "Miami", "avatar_url": "avatars/nathan.jpg"},
            ],
        },
        {
            "id": 3,
            "category_name": "Lojistik ve Depo",
            "persons": [
                {"name": "Olivia Morgan", "position": "HR Specialist", "office": "New York", "avatar_url": "avatars/olivia.jpg"},
                {"name": "Paul Parker", "position": "Recruiter", "office": "San Francisco", "avatar_url": "avatars/paul.jpg"},
                {"name": "Quinn Walker", "position": "HR Manager", "office": "Austin", "avatar_url": "avatars/quinn.jpg"},
                {"name": "Rachel Hill", "position": "Talent Acquisition", "office": "Seattle", "avatar_url": "avatars/rachel.jpg"},
                {"name": "Samuel Young", "position": "Training Coordinator", "office": "Boston", "avatar_url": "avatars/samuel.jpg"},
                {"name": "Tina Bell", "position": "Compensation Analyst", "office": "Chicago", "avatar_url": "avatars/tina.jpg"},
                {"name": "Ursula King", "position": "HR Consultant", "office": "Miami", "avatar_url": "avatars/ursula.jpg"},
            ],
        },
        {
            "id": 4,
            "category_name": "Kafe ve Servis Hizmetleri",
            "persons": [
                {"name": "Olivia Morgan", "position": "HR Specialist", "office": "New York",
                 "avatar_url": "avatars/olivia.jpg"},
                {"name": "Paul Parker", "position": "Recruiter", "office": "San Francisco",
                 "avatar_url": "avatars/paul.jpg"},
                {"name": "Quinn Walker", "position": "HR Manager", "office": "Austin",
                 "avatar_url": "avatars/quinn.jpg"},
                {"name": "Rachel Hill", "position": "Talent Acquisition", "office": "Seattle",
                 "avatar_url": "avatars/rachel.jpg"},
                {"name": "Samuel Young", "position": "Training Coordinator", "office": "Boston",
                 "avatar_url": "avatars/samuel.jpg"},
                {"name": "Tina Bell", "position": "Compensation Analyst", "office": "Chicago",
                 "avatar_url": "avatars/tina.jpg"},
                {"name": "Ursula King", "position": "HR Consultant", "office": "Miami",
                 "avatar_url": "avatars/ursula.jpg"},
            ],
        },
    ]

    return render(request, "candidate_pool_dashboard.html", {"category": categories})
