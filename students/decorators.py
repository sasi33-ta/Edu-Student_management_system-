from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('student_profile')
        return fn(request, *args, **kwargs)
    return wrapper


def student_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return fn(request, *args, **kwargs)
    return wrapper
