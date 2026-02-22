# 🎓 EduManage SMS — Django Student Management System

A full-featured Student Management System built with Django, SQLite, and a modern dark/light UI.

---

## 📋 Features

- **Role-Based Access Control**: Teachers get full CRUD, Students get read-only profile view
- **Admin Dashboard**: Live stat cards, grade distribution charts, recent students
- **Student Management**: Add, view, edit, delete students with search, filter & pagination
- **Profile Photos**: Upload student photos (stored in `/media/profile_pics/`)
- **Dark / Light Mode**: Toggle via the ☀️ button in the topbar — persisted in cookie
- **Responsive Design**: Works on desktop, tablet, and mobile

---

## 🚀 Setup (5 steps)

### Prerequisites
- Python 3.9 or higher
- pip

---

### Step 1 — Extract the project
Unzip `edumanage_sms.zip` to any folder on your computer:
```
edumanage_sms/
├── manage.py
├── setup.py
├── requirements.txt
├── student_management/
├── accounts/
├── students/
├── templates/
└── static/
```

---

### Step 2 — Create a virtual environment
Open a terminal in the project folder and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `Django >= 4.2`
- `Pillow >= 10.0` (for profile photo upload)

---

### Step 4 — Run the one-click setup
```bash
python setup.py
```

This will:
- ✅ Run all database migrations
- ✅ Create the admin account (`admin / admin123`)
- ✅ Create 6 sample students with data

---

### Step 5 — Start the server
```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

---

## 🔑 Login Credentials

| Role            | Username      | Password     |
|-----------------|---------------|--------------|
| 👨‍🏫 Admin/Teacher | `admin`        | `admin123`   |
| 👨‍🎓 Student       | `john.doe`     | `student123` |
| 👨‍🎓 Student       | `jane.smith`   | `student123` |
| 👨‍🎓 Student       | `bob.johnson`  | `student123` |
| 👨‍🎓 Student       | `sarah.wilson` | `student123` |
| 👨‍🎓 Student       | `mike.brown`   | `student123` |
| 👨‍🎓 Student       | `alice.chen`   | `student123` |

---

## 🗂️ Project Structure

```
edumanage_sms/
│
├── manage.py               ← Django management script
├── setup.py                ← One-click setup (migrations + sample data)
├── requirements.txt        ← Python dependencies
│
├── student_management/     ← Core project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/               ← Login / logout
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/login.html
│
├── students/               ← Main app (CRUD, roles, dashboard)
│   ├── models.py           ← Student model (14 fields)
│   ├── views.py            ← All views with role decorators
│   ├── forms.py            ← StudentCreationForm, StudentUpdateForm
│   ├── decorators.py       ← @admin_required, @student_required
│   ├── urls.py
│   └── templates/students/
│       ├── admin_dashboard.html
│       ├── student_list.html
│       ├── student_detail.html
│       ├── student_form.html   ← Add + Edit (same template)
│       └── student_profile.html ← Read-only student view
│
├── templates/              ← Shared templates
│   ├── base.html           ← Master layout (sidebar, topbar, theme toggle)
│   └── errors/
│       ├── 403.html
│       └── 404.html
│
├── static/
│   ├── css/main.css        ← Full design system (dark + light mode)
│   └── js/main.js          ← Theme toggle, photo preview, counters
│
└── media/
    └── profile_pics/       ← Uploaded student photos
```

---

## 🔐 Role-Based Access

| Feature                | Admin/Teacher | Student |
|------------------------|:-------------:|:-------:|
| View dashboard         | ✅            | ❌      |
| View all students      | ✅            | ❌      |
| Add student            | ✅            | ❌      |
| Edit student           | ✅            | ❌      |
| Delete student         | ✅            | ❌      |
| Upload student photo   | ✅            | ❌      |
| View own profile       | ❌            | ✅      |

---

## 🛠️ Additional Commands

Run migrations manually:
```bash
python manage.py migrate
```

Create a new admin:
```bash
python manage.py createsuperuser
```

Django admin panel:
```
http://127.0.0.1:8000/admin/
```

Collect static files (for production):
```bash
python manage.py collectstatic
```

---

## 🌙 Dark / Light Mode

Click the **☀️ / 🌙 button** in the top-right of the topbar to toggle themes.
Your preference is saved in a browser cookie and persists across sessions.

---

## 📸 Profile Photos

When adding or editing a student, click the photo upload area to browse for an image.
Photos are stored in `/media/profile_pics/` and shown in:
- Student list table (thumbnail)
- Student detail view (large avatar)
- Student's own profile page

Supported formats: JPG, PNG, WEBP · Max size: 5 MB

---

*Built with Django 4.2 · SQLite · Syne + Figtree fonts*

## Team Contributions

| Member | Role | Work Done |
|--------|------|-----------|
| sasi33-ta | Backend Core | Models, Views, CRUD, URLs, Settings |
| dixyagharti | Frontend | Templates, Static files, UI Design |
| swas26tika | Accounts | Authentication, Login, Logout |
