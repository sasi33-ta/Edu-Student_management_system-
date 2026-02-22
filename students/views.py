from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import Student
from .forms import StudentCreationForm, StudentUpdateForm
from .decorators import admin_required, student_required


# ── ROUTER ────────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('student_profile')


# ── ADMIN DASHBOARD ───────────────────────────────────────────────────────────
@admin_required
def admin_dashboard(request):
    students = Student.objects.select_related('user').all()
    total    = students.count()
    active   = students.filter(status='active').count()
    inactive = students.filter(status='inactive').count()
    recent   = students[:6]

    grade_counts = {}
    for s in students:
        grade_counts[s.grade_display] = grade_counts.get(s.grade_display, 0) + 1
    grade_data = sorted(grade_counts.items(), key=lambda x: -x[1])
    max_grade  = grade_data[0][1] if grade_data else 1

    return render(request, 'students/admin_dashboard.html', {
        'total': total, 'active': active, 'inactive': inactive,
        'recent': recent, 'grade_data': grade_data, 'max_grade': max_grade,
    })


# ── STUDENT LIST ──────────────────────────────────────────────────────────────
@admin_required
def student_list(request):
    qs = Student.objects.select_related('user').all()
    q       = request.GET.get('q', '').strip()
    grade   = request.GET.get('grade', '')
    section = request.GET.get('section', '')
    status  = request.GET.get('status', '')

    if q:
        qs = qs.filter(Q(full_name__icontains=q)|Q(roll_number__icontains=q)|
                       Q(email__icontains=q)|Q(phone__icontains=q))
    if grade:   qs = qs.filter(grade=grade)
    if section: qs = qs.filter(section=section)
    if status:  qs = qs.filter(status=status)

    paginator = Paginator(qs, 10)
    page_obj  = paginator.get_page(request.GET.get('page'))

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj, 'q': q, 'grade': grade,
        'section': section, 'status': status,
        'total_count': qs.count(),
        'grade_choices':   Student.GRADE_CHOICES,
        'section_choices': Student.SECTION_CHOICES,
        'status_choices':  Student.STATUS_CHOICES,
    })


# ── STUDENT DETAIL ────────────────────────────────────────────────────────────
@admin_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


# ── ADD STUDENT ───────────────────────────────────────────────────────────────
@admin_required
def student_add(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            s = form.save()
            messages.success(request, f'✅ Student "{s.full_name}" added! Login: {s.user.username}')
            return redirect('student_list')
    else:
        form = StudentCreationForm()
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Add'})


# ── EDIT STUDENT ──────────────────────────────────────────────────────────────
@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            s = form.save()
            s.user.email = s.email
            s.user.save()
            messages.success(request, f'✅ Student "{s.full_name}" updated successfully.')
            return redirect('student_detail', pk=s.pk)
    else:
        form = StudentUpdateForm(instance=student)
    return render(request, 'students/student_form.html', {
        'form': form, 'action': 'Edit', 'student': student
    })


# ── DELETE STUDENT ────────────────────────────────────────────────────────────
@admin_required
@require_POST
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    name = student.full_name
    user = student.user
    student.delete()
    user.delete()
    messages.success(request, f'🗑 Student "{name}" has been permanently deleted.')
    return redirect('student_list')


# ── STUDENT SELF-PROFILE ──────────────────────────────────────────────────────
@student_required
def student_profile(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Profile not found. Contact your administrator.')
        return redirect('login')
    return render(request, 'students/student_profile.html', {'student': student})


# ── THEME TOGGLE ──────────────────────────────────────────────────────────────
@login_required
def toggle_theme(request):
    if request.method == 'POST':
        current   = request.COOKIES.get('theme', 'dark')
        new_theme = 'light' if current == 'dark' else 'dark'
        response  = JsonResponse({'theme': new_theme})
        response.set_cookie('theme', new_theme, max_age=365*24*60*60)
        return response
    return JsonResponse({'error': 'POST required'}, status=405)


# ── ERROR PAGES ───────────────────────────────────────────────────────────────
def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)
