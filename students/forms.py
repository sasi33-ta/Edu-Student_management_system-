from django import forms
from django.contrib.auth.models import User
from .models import Student

WIDGET_ATTRS = {'class': 'form-control'}
SELECT_ATTRS = {'class': 'form-select'}


class StudentCreationForm(forms.ModelForm):
    username  = forms.CharField(max_length=150, widget=forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. john.doe'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Min 8 characters'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Repeat password'}))

    class Meta:
        model  = Student
        fields = ['full_name','email','phone','date_of_birth','gender','address',
                  'grade','section','roll_number','admission_date','status','profile_pic']
        widgets = {
            'full_name':     forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Full name'}),
            'email':         forms.EmailInput(attrs={**WIDGET_ATTRS, 'placeholder': 'student@email.com'}),
            'phone':         forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '+1-555-0101'}),
            'date_of_birth': forms.DateInput(attrs={**WIDGET_ATTRS, 'type': 'date'}),
            'gender':        forms.Select(attrs=SELECT_ATTRS),
            'address':       forms.Textarea(attrs={**WIDGET_ATTRS, 'rows': 2, 'placeholder': 'Address'}),
            'grade':         forms.Select(attrs=SELECT_ATTRS),
            'section':       forms.Select(attrs=SELECT_ATTRS),
            'roll_number':   forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '2024001'}),
            'admission_date':forms.DateInput(attrs={**WIDGET_ATTRS, 'type': 'date'}),
            'status':        forms.Select(attrs=SELECT_ATTRS),
            'profile_pic':   forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_username(self):
        u = self.cleaned_data['username'].strip()
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('This username is already taken.')
        return u

    def clean_email(self):
        e = self.cleaned_data['email'].strip()
        if Student.objects.filter(email=e).exists():
            raise forms.ValidationError('A student with this email already exists.')
        return e

    def clean_roll_number(self):
        r = self.cleaned_data['roll_number'].strip()
        if Student.objects.filter(roll_number=r).exists():
            raise forms.ValidationError('This roll number is already assigned.')
        return r

    def clean(self):
        cd = super().clean()
        p1, p2 = cd.get('password1'), cd.get('password2')
        if p1 and p2:
            if p1 != p2:
                self.add_error('password2', 'Passwords do not match.')
            elif len(p1) < 8:
                self.add_error('password1', 'Password must be at least 8 characters.')
        return cd

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['full_name','email','phone','date_of_birth','gender','address',
                  'grade','section','roll_number','admission_date','status','profile_pic']
        widgets = {
            'full_name':     forms.TextInput(attrs=WIDGET_ATTRS),
            'email':         forms.EmailInput(attrs=WIDGET_ATTRS),
            'phone':         forms.TextInput(attrs=WIDGET_ATTRS),
            'date_of_birth': forms.DateInput(attrs={**WIDGET_ATTRS, 'type': 'date'}),
            'gender':        forms.Select(attrs=SELECT_ATTRS),
            'address':       forms.Textarea(attrs={**WIDGET_ATTRS, 'rows': 2}),
            'grade':         forms.Select(attrs=SELECT_ATTRS),
            'section':       forms.Select(attrs=SELECT_ATTRS),
            'roll_number':   forms.TextInput(attrs=WIDGET_ATTRS),
            'admission_date':forms.DateInput(attrs={**WIDGET_ATTRS, 'type': 'date'}),
            'status':        forms.Select(attrs=SELECT_ATTRS),
            'profile_pic':   forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_email(self):
        e = self.cleaned_data['email'].strip()
        if Student.objects.filter(email=e).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A student with this email already exists.')
        return e

    def clean_roll_number(self):
        r = self.cleaned_data['roll_number'].strip()
        if Student.objects.filter(roll_number=r).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This roll number is already assigned.')
        return r
