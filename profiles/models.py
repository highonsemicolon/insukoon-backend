from django.conf import settings
from django.db import models


class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    # Student details
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    student_dob = models.DateField(default='2005-11-01')
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

    # Session Details
    preferred_start_date = models.DateField(auto_now_add=True, null=True, blank=True)
    batch_day = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ], default='Monday')
    batch_time = models.CharField(max_length=20, choices=[
        ('4:00 PM - 5:00 PM', '4:00 PM - 5:00 PM'),
        ('5:00 PM - 6:00 PM', '5:00 PM - 6:00 PM'),
        ('6:00 PM - 7:00 PM', '6:00 PM - 7:00 PM'),
        ('7:00 PM - 8:00 PM', '7:00 PM - 8:00 PM'),
        ('8:00 PM - 9:00 PM', '8:00 PM - 9:00 PM'),
    ], default='4:00 PM - 5:00')
    preferred_language = models.CharField(max_length=20, choices=[
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Mix of Both', 'Mix of Both'),
    ], default='Mix of Both')

    areas_to_improve_in_child_1 = models.TextField(blank=True)
    areas_to_improve_in_child_2 = models.TextField(blank=True)
    areas_to_improve_in_child_3 = models.TextField(blank=True)
    areas_to_improve_in_child_4 = models.TextField(blank=True)
    areas_to_improve_in_child_5 = models.TextField(blank=True)

    areas_to_improve_as_parent_1 = models.TextField(blank=True)
    areas_to_improve_as_parent_2 = models.TextField(blank=True)
    areas_to_improve_as_parent_3 = models.TextField(blank=True)

    session_day = models.CharField(max_length=10, choices=[
        ('Weekday', 'Weekday'),
        ('Weekend', 'Weekend'),
    ], default='Weekday')
    session_time = models.CharField(max_length=20, choices=[
        ('Before 8 PM', 'Before 8 PM'),
        ('After 8 PM', 'After 8 PM'),
    ], default='After 8 PM')

    def __str__(self):
        return f"Parent Profile: {self.user}"


class SchoolProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # School details
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
    total_students = models.PositiveIntegerField(default=1)
    avg_class_size = models.PositiveIntegerField(default=0)
    kg_students = models.PositiveIntegerField(default=0)
    grade_1_5_students = models.PositiveIntegerField(default=0)
    grade_6_8_students = models.PositiveIntegerField(default=0)
    grade_9_12_students = models.PositiveIntegerField(default=0)

    # Staff details
    total_teachers = models.PositiveIntegerField(default=0)
    total_non_teaching_staff = models.PositiveIntegerField(default=0)
    kg_teachers = models.PositiveIntegerField(default=0)
    grade_1_5_teachers = models.PositiveIntegerField(default=0)
    grade_6_8_teachers = models.PositiveIntegerField(default=0)
    grade_9_12_teachers = models.PositiveIntegerField(default=0)

    # Program details
    PROGRAM_CHOICES = [
        ('Kindergarten', 'Kindergarten'),
        ('Primary', 'Primary Schooler (Grade 1-5)'),
        ('PreTeens', 'Pre-Teens (6-8)'),
        ('Teens', 'Teens (9-10)')
    ]
    program_1_name = models.CharField(max_length=100, choices=PROGRAM_CHOICES, null=True, blank=True)
    program_1_student_session_day = models.CharField(max_length=100,
                                                     choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                              ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                              ('Friday', 'Friday')], null=True, blank=True)
    program_1_student_batch_time = models.CharField(max_length=100, choices=[('During', 'During School Hours'),
                                                                             ('After', 'After School Hours')],
                                                    null=True, blank=True)

    program_2_name = models.CharField(max_length=100, choices=[('Gurutva', 'Gurutva (Teacher\'s Program)'),
                                                               ('Samarpan', 'Samarpan (Staff Program)')], null=True,
                                      blank=True)
    program_2_teacher_session_day = models.CharField(max_length=100,
                                                     choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                              ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                              ('Friday', 'Friday')], null=True, blank=True)
    program_2_teacher_batch_time = models.CharField(max_length=100, choices=[('During', 'During School Hours'),
                                                                             ('After', 'After School Hours')],
                                                    null=True, blank=True)
    program_2_staff_session_day = models.CharField(max_length=100,
                                                   choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                            ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                            ('Friday', 'Friday')], null=True, blank=True)
    program_2_staff_batch_time = models.CharField(max_length=100, choices=[('During', 'During School Hours'),
                                                                           ('After', 'After School Hours')], null=True,
                                                  blank=True)

    def __str__(self):
        return f"School Profile: {self.name}"
