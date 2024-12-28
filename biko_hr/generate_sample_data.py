from django.contrib.auth.models import User
from biko_hr.models import (
    Profile, Location, Organization, JobCategory, Position, Candidate,
    IncubationJob, Application, Interview, Notification, Evaluation,
    InterviewAttributes, IncubationEvaluation, IncubationAttributes, Reference
)
from datetime import date

# # Create Users
# user1 = User.objects.create_user(username="johndoe", email="johndoe@example.com", password="password123")
# user2 = User.objects.create_user(username="janedoe", email="janedoe@example.com", password="password123")
#
# # Create Profiles
# Profile.objects.create(user=user1, profile_picture="profile_pictures/johndoe.jpg")
# Profile.objects.create(user=user2, profile_picture="profile_pictures/janedoe.jpg")
#
# # Create Locations
# location1 = Location.objects.create(location="New York")
# location2 = Location.objects.create(location="San Francisco")
#
# # Create Organizations
# org1 = Organization.objects.create(organization="TechCorp", location=location1)
# org2 = Organization.objects.create(organization="InnovateInc", location=location2)
#
# # Create Job Categories
# category1 = JobCategory.objects.create(category_name="Software Development")
# category2 = JobCategory.objects.create(category_name="Data Science")
#
# # Create Positions
# position1 = Position.objects.create(position="Software Engineer", category=category1)
# position2 = Position.objects.create(position="Data Scientist", category=category2)
#
#
# # Create Candidates
# candidate1 = Candidate.objects.create(
#     name="John", surname="Smith", email="johnsmith@example.com", phone="1234567890",
#     experience="5 years in software development", skills="Python, Django, React",
#     birth_date="1990-01-01", residence_city="New York", residence_district="Manhattan",
#     education_level="Bachelor's", school_name="MIT", department="Computer Science"
# )
#
# candidate2 = Candidate.objects.create(
#     name="Jane", surname="Doe", email="janedoe@example.com", phone="0987654321",
#     experience="3 years in data science", skills="Python, Machine Learning, SQL",
#     birth_date="1995-05-15", residence_city="San Francisco", residence_district="Mission District",
#     education_level="Master's", school_name="Stanford", department="Data Science"
# )
#
# Create Incubation Jobs
incubation_job1 = IncubationJob.objects.create(
    organization=Organization.objects.get(id=1), position=Position.objects.get(id=1), category= JobCategory.objects.get(id=1),title="AI Engineer", description="Build AI models", required_skills="Python, TensorFlow",
    status="Open", preferred_locations="New York", department="AI Research"
)

incubation_job2 = IncubationJob.objects.create(
    organization=Organization.objects.get(id=2), position=Position.objects.get(id=2), category= JobCategory.objects.get(id=2),title="Backend Developer", description="Develop backend APIs", required_skills="Django, Flask",
    status="Open", preferred_locations="San Francisco", department="Software Engineering"
)
#
# Create Applications
application1 = Application.objects.create(
    candidate=Candidate.objects.get(id=1), job=incubation_job1, application_date=date.today(),
    status="Pending", uploaded_resume="resumes/johnsmith.pdf"
)

application2 = Application.objects.create(
    candidate=Candidate.objects.get(id=2), job=incubation_job2, application_date=date.today(),
    status="Pending", uploaded_resume="resumes/janedoe.pdf"
)
#
# # Create Notifications
# Notification.objects.create(user=user1, message="Your application has been received", status="Unread")
# Notification.objects.create(user=user2, message="Your application has been reviewed", status="Read")
#
# # Create References
# Reference.objects.create(
#     candidate=candidate1, reference_name="Alice Brown", reference_role="Manager",
#     reference_company="TechCorp", reference_phone="1231231234", work_duration="2 years",
#     duties="Developed software applications", strengths="Problem-solving", weaknesses="Time management",
#     reason_for_leaving="Better opportunity", would_work_again=True
# )
#
# Reference.objects.create(
#     candidate=candidate2, reference_name="Bob Green", reference_role="Team Lead",
#     reference_company="InnovateInc", reference_phone="3213214321", work_duration="1 year",
#     duties="Analyzed datasets", strengths="Detail-oriented", weaknesses="Presentation skills",
#     reason_for_leaving="Relocation", would_work_again=True
# )
# # Fetch existing locations
# new_york = Location.objects.filter(location="New York").first()
# san_francisco = Location.objects.filter(location="San Francisco").first()
# austin = Location.objects.filter(location="Austin").first()
# seattle = Location.objects.filter(location="Seattle").first()
# boston = Location.objects.filter(location="Boston").first()
# chicago = Location.objects.filter(location="Chicago").first()
# miami = Location.objects.filter(location="Miami").first()
#
# # This ensures that if there are multiple entries, only the first one is used.
# # If there are no locations found, it will return None.
#
# # Add Organizations
# techcorp = Organization.objects.create(organization="TechCorp", location=new_york)
# innovateinc = Organization.objects.create(organization="InnovateInc", location=san_francisco)
#
# # Fetch existing Job Categories or create if they don't exist
# category1 = JobCategory.objects.filter(category_name="Operasyon ve Destek").first()
# if not category1:
#     category1 = JobCategory.objects.create(category_name="Operasyon ve Destek")
#
# category2 = JobCategory.objects.filter(category_name="Gıda ve Yemek Hizmetleri").first()
# if not category2:
#     category2 = JobCategory.objects.create(category_name="Gıda ve Yemek Hizmetleri")
#
# category3 = JobCategory.objects.filter(category_name="Lojistik ve Depo").first()
# if not category3:
#     category3 = JobCategory.objects.create(category_name="Lojistik ve Depo")
#
# # Add Positions (These positions are fetched from existing categories)
# position1 = Position.objects.create(position="Backend Developer", category=category1)
# position2 = Position.objects.create(position="Frontend Developer", category=category1)
# position3 = Position.objects.create(position="Full-Stack Developer", category=category1)
# position4 = Position.objects.create(position="DevOps Engineer", category=category1)
# position5 = Position.objects.create(position="QA Engineer", category=category1)
# position6 = Position.objects.create(position="Software Architect", category=category1)
# position7 = Position.objects.create(position="Mobile Developer", category=category1)
#
# position8 = Position.objects.create(position="Data Scientist", category=category2)
# position9 = Position.objects.create(position="Machine Learning Engineer", category=category2)
# position10 = Position.objects.create(position="AI Researcher", category=category2)
# position11 = Position.objects.create(position="Data Analyst", category=category2)
# position12 = Position.objects.create(position="Big Data Engineer", category=category2)
# position13 = Position.objects.create(position="Statistician", category=category2)
# position14 = Position.objects.create(position="Data Engineer", category=category2)
#
# position15 = Position.objects.create(position="HR Specialist", category=category3)
# position16 = Position.objects.create(position="Recruiter", category=category3)
# position17 = Position.objects.create(position="HR Manager", category=category3)
# position18 = Position.objects.create(position="Talent Acquisition", category=category3)
# position19 = Position.objects.create(position="Training Coordinator", category=category3)
# position20 = Position.objects.create(position="Compensation Analyst", category=category3)
# position21 = Position.objects.create(position="HR Consultant", category=category3)
#
# # Create Candidates for each person in each category
#
# # Operasyon ve Destek (Category 1)
# person_data_category1 = [
#     {"name": "Alice Smith", "position": position1, "office": new_york},
#     {"name": "Bob Johnson", "position": position2, "office": san_francisco},
#     {"name": "Charlie Davis", "position": position3, "office": austin},
#     {"name": "Diana Lee", "position": position4, "office": seattle},
#     {"name": "Evan Garcia", "position": position5, "office": boston},
#     {"name": "Fiona Brown", "position": position6, "office": chicago},
#     {"name": "George White", "position": position7, "office": miami},
# ]
#
# for person in person_data_category1:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
#
# # Gıda ve Yemek Hizmetleri (Category 2)
# person_data_category2 = [
#     {"name": "Hannah Green", "position": position8, "office": new_york},
#     {"name": "Ian Black", "position": position9, "office": san_francisco},
#     {"name": "Jack Brown", "position": position10, "office": austin},
#     {"name": "Karen Gray", "position": position11, "office": seattle},
#     {"name": "Liam Carter", "position": position12, "office": boston},
#     {"name": "Mia Lopez", "position": position13, "office": chicago},
#     {"name": "Nathan Scott", "position": position14, "office": miami},
# ]
#
# for person in person_data_category2:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
#
# # Lojistik ve Depo (Category 3)
# person_data_category3 = [
#     {"name": "Olivia Morgan", "position": position15, "office": new_york},
#     {"name": "Paul Parker", "position": position16, "office": san_francisco},
#     {"name": "Quinn Walker", "position": position17, "office": austin},
#     {"name": "Rachel Hill", "position": position18, "office": seattle},
#     {"name": "Samuel Young", "position": position19, "office": boston},
#     {"name": "Tina Bell", "position": position20, "office": chicago},
#     {"name": "Ursula King", "position": position21, "office": miami},
# ]
#
# for person in person_data_category3:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
########
# # Locations to be added
# locations = [
#     "ADANA", "ACIBADEM ÜNİVERSİTESİ", "ALTUNİZADE", "ANKARA", "ATAKENT", "ATAŞEHİR", "BAKIRKÖY", "BODRUM", "BURSA",
#     "ESKİŞEHİR", "FULYA", "INTERNATIONAL HOSPITAL", "KADIKÖY", "KARTAL", "KAYSERİ", "KENT", "KOZYATAĞI", "MASLAK",
#     "ORTAPEDİA", "TAKSİM", "ATAŞEHİR TIP", "BAĞDAT", "BAHÇEŞEHİR", "BAYRAKLI", "BEYLİKDÜZÜ", "BODRUM TIP", "ETİLER",
#     "GEBZE FABRİKA", "GENEL MÜDÜRLÜK", "GÖKTÜRK", "SAMANDIRA", "ZEKERİYAKÖY", "DIŞ PROJE", "YONCA TEKNİK", "TED",
#     "TÜRKİYE SİNAİ VE KALKINMA BANKASI", "SZA OMICS", "Özel NPİ Nöropsikiyatri", "PATALOJİ", "POLAT TOWERS",
#     "ROMAN GİYİM", "NİŞANTAŞI PATALOJİ", "LABMED", "HAVELSAN", "ESTELİT", "ELMAS ÇAMAŞIR", "ERSE KABLO",
#     "ACIBADEM PROJE YÖNETİMİ", "ACIBADEM SPORTS", "ACIBADEM SİGORTA", "KOŞUYOLU ÖZELİM", "ALİFE"
# ]
#
# # Add Locations to DB
# for location in locations:
#     Location.objects.get_or_create(location=location)
#
# # Organizations to be added
# organizations = [
#     ("Entegre Kalite Yönetim Sistemleri Müdürlüğü", "ADANA"),
#     ("Temizlik Hizmetleri Operasyon Direktörlüğü", "KADIKÖY"),
#     ("Kafe Hizmetleri Direktörlüğü", "MASLAK"),
#     ("Bordro ve Özlük İşleri Müdürlüğü", "ATAŞEHİR"),
#     ("Gider Yönetimi Müdürlüğü", "ANKARA"),
#     ("İç Denetim Koordinatörlüğü", "BODRUM"),
#     ("İdari İşler ve Güvenlik Müdürlüğü", "BURSA"),
#     ("İnsan Kaynakları Müdürlüğü", "ESKİŞEHİR"),
#     ("İşyeri Hekimliği Müdürlüğü", "FULYA"),
#     ("Lojistik Müdürlüğü", "GENEL MÜDÜRLÜK"),
#     ("Mali İşler Müdürlüğü", "GÖKTÜRK"),
#     ("Pazarlama ve Kurumsal İletişim Müdürlüğü", "SAMANDIRA"),
#     ("Planlama ve Maliyet Yönetimi Direktör Yardımcılığı", "ZEKERİYAKÖY"),
#     ("Tesis Yönetimi", "KOZYATAĞI"),
#     ("Satınalma Direktörlüğü", "BODRUM TIP"),
#     ("Teknik Hizmetler Müdürlüğü", "ETİLER"),
#     ("Bilgi Teknolojileri Müdürlüğü", "INTERNATIONAL HOSPITAL"),
#     ("Diyet ve Toplu Yemek Hizmetleri Direktörlüğü", "KAYSERİ"),
#     ("Depo Hizmetleri Müdürlüğü", "KARTAL"),
#     ("Fabrika Hizmetleri Müdürlüğü", "SAMANDIRA"),
#     ("İş Güvenliği Müdürlüğü", "TAKSİM"),
#     ("Kafe Hizmetleri Direktörlüğü", "BAYRAKLI"),
#     ("Teknik Tekstil ve Çamaşırhane Direktörlüğü", "GEBZE FABRİKA"),
#     ("Temizlik Hizmetleri Operasyon Direktörlüğü", "BODRUM"),
# ]
#
# # Add Organizations to DB and associate with Locations
# for org_name, location_name in organizations:
#     location = Location.objects.get(location=location_name)
#     Organization.objects.get_or_create(organization=org_name, location=location)
#
# # Fetch Categories for data generation
# category1 = JobCategory.objects.filter(category_name="Operasyon ve Destek").first()
# if not category1:
#     category1 = JobCategory.objects.create(category_name="Operasyon ve Destek")
#
# category2 = JobCategory.objects.filter(category_name="Gıda ve Yemek Hizmetleri").first()
# if not category2:
#     category2 = JobCategory.objects.create(category_name="Gıda ve Yemek Hizmetleri")
#
# category3 = JobCategory.objects.filter(category_name="Lojistik ve Depo").first()
# if not category3:
#     category3 = JobCategory.objects.create(category_name="Lojistik ve Depo")
#
# # Add Positions for categories (using fetched categories)
# position1 = Position.objects.create(position="Backend Developer", category=category1)
# position2 = Position.objects.create(position="Frontend Developer", category=category1)
# position3 = Position.objects.create(position="Full-Stack Developer", category=category1)
# position4 = Position.objects.create(position="DevOps Engineer", category=category1)
#
# position5 = Position.objects.create(position="Data Scientist", category=category2)
# position6 = Position.objects.create(position="Machine Learning Engineer", category=category2)
# position7 = Position.objects.create(position="AI Researcher", category=category2)
#
# position8 = Position.objects.create(position="HR Specialist", category=category3)
# position9 = Position.objects.create(position="Recruiter", category=category3)
# position10 = Position.objects.create(position="HR Manager", category=category3)
#
# # Generate Candidates for each category with assigned locations and organizations
#
# # Operasyon ve Destek (Category 1)
# person_data_category1 = [
#     {"name": "Alice Smith", "position": position1, "office": Location.objects.get(location="ADANA")},
#     {"name": "Bob Johnson", "position": position2, "office": Location.objects.get(location="ANKARA")},
#     {"name": "Charlie Davis", "position": position3, "office": Location.objects.get(location="ATAKENT")},
# ]
#
# for person in person_data_category1:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
#
# # Gıda ve Yemek Hizmetleri (Category 2)
# person_data_category2 = [
#     {"name": "Hannah Green", "position": position5, "office": Location.objects.get(location="BODRUM")},
#     {"name": "Ian Black", "position": position6, "office": Location.objects.get(location="KADIKÖY")},
#     {"name": "Jack Brown", "position": position7, "office": Location.objects.get(location="MASLAK")},
# ]
#
# for person in person_data_category2:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
#
# # Lojistik ve Depo (Category 3)
# person_data_category3 = [
#     {"name": "Olivia Morgan", "position": position8, "office": Location.objects.get(location="BAKIRKÖY")},
#     {"name": "Paul Parker", "position": position9, "office": Location.objects.get(location="BURSA")},
#     {"name": "Quinn Walker", "position": position10, "office": Location.objects.get(location="ESKİŞEHİR")},
# ]
#
# for person in person_data_category3:
#     Candidate.objects.create(
#         name=person["name"],
#         surname=person["name"].split()[1],  # Assuming surname is the second part of the name
#         email=person["name"].lower().replace(" ", "") + "@example.com",
#         phone="1234567890",
#         experience="Experience data",
#         skills="Skills data",
#         birth_date="1990-01-01",
#         residence_city=person["office"].location,
#         residence_district="District data",
#         education_level="Education data",
#         school_name="School name",
#         department="Department data"
#     )
#
print("Sample data added successfully.")