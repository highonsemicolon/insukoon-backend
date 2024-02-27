from django.contrib.auth.models import User
from django.db import models


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Student details
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    student_dob = models.DateField()
    student_gender = models.CharField(max_length=10)
    student_country = models.CharField(max_length=100)
    student_state = models.CharField(max_length=100)
    student_grade = models.CharField(max_length=100)

    # Father details
    father_first_name = models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100)
    father_email = models.EmailField()
    father_mobile_number = models.CharField(max_length=20)
    father_occupation = models.CharField(max_length=100)

    # Mother details
    mother_first_name = models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100)
    mother_email = models.EmailField()
    mother_mobile_number = models.CharField(max_length=20)
    mother_occupation = models.CharField(max_length=100)

    # Verification details
    mobile_number_verification = models.BooleanField(default=False)
    email_verification = models.BooleanField(default=False)

    def __str__(self):
        return f"Parent Profile: {self.user.username}"


class SchoolProfile(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    zip_code = models.CharField(max_length=20)
    classes_start_from = models.CharField(max_length=100)
    classes_end_to = models.CharField(max_length=100)
    level = models.CharField(max_length=100)

    # Contact details
    director_name = models.CharField(max_length=100)
    director_phone_number = models.CharField(max_length=20)
    director_email = models.EmailField()
    principal_name = models.CharField(max_length=100)
    principal_phone_number = models.CharField(max_length=20)
    principal_email = models.EmailField()
    poc_name = models.CharField(max_length=100)
    poc_mobile_number = models.CharField(max_length=20)
    poc_email = models.EmailField()

    # Student details
    total_students = models.PositiveIntegerField()
    avg_class_size = models.PositiveIntegerField()
    kg_students = models.PositiveIntegerField()
    grade_1_5_students = models.PositiveIntegerField()
    grade_6_8_students = models.PositiveIntegerField()
    grade_9_12_students = models.PositiveIntegerField()

    # Staff details
    total_teachers = models.PositiveIntegerField()
    total_non_teaching_staff = models.PositiveIntegerField()
    kg_teachers = models.PositiveIntegerField()
    grade_1_5_teachers = models.PositiveIntegerField()
    grade_6_8_teachers = models.PositiveIntegerField()
    grade_9_12_teachers = models.PositiveIntegerField()

    def __str__(self):
        return f"School Profile: {self.name}"
