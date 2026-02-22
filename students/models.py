from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Student(models.Model):
    GENDER_CHOICES  = [('M','Male'),('F','Female'),('O','Other')]
    GRADE_CHOICES   = [
        ('1','Grade 1'),('2','Grade 2'),('3','Grade 3'),('4','Grade 4'),
        ('5','Grade 5'),('6','Grade 6'),('7','Grade 7'),('8','Grade 8'),
        ('9','Grade 9'),('10','Grade 10'),('11','Grade 11'),('12','Grade 12'),
        ('UG1','UG Year 1'),('UG2','UG Year 2'),('PG','Post Graduate'),
    ]
    SECTION_CHOICES = [('A','A'),('B','B'),('C','C'),('D','D'),('E','E')]
    STATUS_CHOICES  = [('active','Active'),('inactive','Inactive')]

    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    full_name      = models.CharField(max_length=150)
    email          = models.EmailField(unique=True)
    phone          = models.CharField(max_length=20, blank=True)
    date_of_birth  = models.DateField(null=True, blank=True)
    gender         = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address        = models.TextField(blank=True)
    grade          = models.CharField(max_length=4, choices=GRADE_CHOICES)
    section        = models.CharField(max_length=1, choices=SECTION_CHOICES, default='A')
    roll_number    = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField(null=True, blank=True)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_pic    = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        b = self.date_of_birth
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    @property
    def grade_display(self):
        return dict(self.GRADE_CHOICES).get(self.grade, self.grade)
