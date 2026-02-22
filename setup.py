#!/usr/bin/env python
"""
EduManage SMS — One-click setup script
Run: python setup.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n🎓 EduManage SMS — Setup\n" + "="*40)

    # ── Run migrations ──────────────────────────────
    print("\n[1/3] Running database migrations...")
    from django.core.management import call_command
    django.setup()
    call_command('migrate', '--run-syncdb', verbosity=0)
    print("    ✅ Database ready")

    from django.contrib.auth.models import User
    from students.models import Student

    # ── Create admin ────────────────────────────────
    print("\n[2/3] Creating admin account...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@edumanage.com', 'admin123')
        print("    ✅ Admin created  →  admin / admin123")
    else:
        print("    ℹ️  Admin already exists")

    # ── Create sample students ─────────────────────
    print("\n[3/3] Creating sample students...")
    samples = [
        {'username':'john.doe',   'password':'student123','full_name':'John Doe',
         'email':'john.doe@school.edu',  'phone':'+1-555-0101','dob':'2005-03-15',
         'gender':'M','address':'123 Main St, New York, NY',
         'grade':'10','section':'A','roll':'2024001','status':'active'},
        {'username':'jane.smith', 'password':'student123','full_name':'Jane Smith',
         'email':'jane.smith@school.edu','phone':'+1-555-0102','dob':'2005-07-22',
         'gender':'F','address':'456 Oak Ave, Boston, MA',
         'grade':'10','section':'B','roll':'2024002','status':'active'},
        {'username':'bob.johnson','password':'student123','full_name':'Bob Johnson',
         'email':'bob.j@school.edu',    'phone':'+1-555-0103','dob':'2004-11-08',
         'gender':'M','address':'789 Pine Rd, Chicago, IL',
         'grade':'11','section':'A','roll':'2023001','status':'active'},
        {'username':'sarah.wilson','password':'student123','full_name':'Sarah Wilson',
         'email':'sarah.w@school.edu',  'phone':'+1-555-0104','dob':'2006-01-30',
         'gender':'F','address':'321 Elm St, Houston, TX',
         'grade':'9', 'section':'C','roll':'2025001','status':'active'},
        {'username':'mike.brown', 'password':'student123','full_name':'Mike Brown',
         'email':'mike.b@school.edu',   'phone':'+1-555-0105','dob':'2004-05-12',
         'gender':'M','address':'654 Maple Dr, Phoenix, AZ',
         'grade':'12','section':'B','roll':'2022001','status':'inactive'},
        {'username':'alice.chen', 'password':'student123','full_name':'Alice Chen',
         'email':'alice.c@school.edu',  'phone':'+1-555-0106','dob':'2005-09-03',
         'gender':'F','address':'987 Cedar Ln, Seattle, WA',
         'grade':'10','section':'A','roll':'2024003','status':'active'},
    ]

    from datetime import date
    created = 0
    for s in samples:
        if not User.objects.filter(username=s['username']).exists():
            user = User.objects.create_user(
                username=s['username'], password=s['password'], email=s['email']
            )
            Student.objects.create(
                user=user, full_name=s['full_name'], email=s['email'],
                phone=s['phone'], date_of_birth=s['dob'],
                gender=s['gender'], address=s['address'],
                grade=s['grade'], section=s['section'],
                roll_number=s['roll'], status=s['status'],
                admission_date='2021-09-01',
            )
            created += 1

    if created:
        print(f"    ✅ Created {created} sample students (password: student123)")
    else:
        print("    ℹ️  Sample students already exist")

    print("\n" + "="*40)
    print("✅ Setup complete!\n")
    print("📌 Login credentials:")
    print("   Admin   →  admin / admin123")
    print("   Student →  john.doe / student123")
    print("            →  jane.smith / student123")
    print("\n🚀 Start server:  python manage.py runserver")
    print("🌐 Open browser:  http://127.0.0.1:8000/\n")

if __name__ == '__main__':
    main()
