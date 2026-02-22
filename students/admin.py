from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ['full_name','roll_number','grade','section','status','created_at']
    list_filter    = ['grade','section','status','gender']
    search_fields  = ['full_name','roll_number','email']
    readonly_fields= ['created_at','updated_at']
