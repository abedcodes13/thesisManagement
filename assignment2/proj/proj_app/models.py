from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('supervisor', 'Supervisor'),
        ('group', 'Group'),
        ('student', 'Student'),
        ('unit_coordinator', 'Unit Coordinator'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

class UnitCoordinatorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class SupervisorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    group = models.ForeignKey('GroupProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.user.username

class GroupProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.ForeignKey('Topic', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='groups')

    def __str__(self):
        return self.name

    def clean(self):
        if self.students.count() < 3 or self.students.count() > 5:
            raise ValidationError('A group must consist of three to five students.')

class Topic(models.Model):
    CATEGORY_CHOICES = [
        ('AI_ML_DS', 'Artificial Intelligence, Machine Learning and Data Science'),
        ('BIOMED', 'Biomedical Engineering and Health Informatics'),
        ('CYBER_SEC', 'Cyber Security'),
        ('ML_DS', 'Machine Learning and Data Science'),
    ]    
    topicID = models.CharField(max_length=4, primary_key=True)
    title = models.CharField(max_length=90)
    description = models.CharField(max_length=1500)
    brief_description = models.CharField(max_length=700)
    category = models.CharField(max_length=80, choices=CATEGORY_CHOICES)
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.SET_NULL, related_name='topics', null=True)
    group_limit = models.PositiveIntegerField(default=3)
    cas = models.BooleanField(default=False)
    syd = models.BooleanField(default=False)
    external = models.BooleanField(default=False)
    chem_eng = models.BooleanField(default=False)
    cns_eng = models.BooleanField(default=False)
    eee = models.BooleanField(default=False)
    mech_eng = models.BooleanField(default=False)
    cs = models.BooleanField(default=False)
    cyb_sec = models.BooleanField(default=False)
    data_sc = models.BooleanField(default=False)
    is_ds = models.BooleanField(default=False)
    seng = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    removal_requested = models.BooleanField(default=False)
    pending_approval = models.BooleanField(default=False)  # New field for pending approval


    def __str__(self):
        return self.topicID + ': ' + self.title
    
    def current_group_count(self):
        return self.groups.count()

class Application(models.Model):
    groupID = models.ForeignKey(GroupProfile, on_delete=models.CASCADE, related_name='applications')
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    supervisor_approval = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + " : " + str(self.groupID) + " applied for topic number " + str(self.topicID.topicID)

    def clean(self):
        if self.groupID.students.count() < 3 or self.groupID.students.count() > 5:
            raise ValidationError('A group must consist of three to five students to apply for a topic.')
        if Application.objects.filter(groupID=self.groupID, topicID=self.topicID).exists():
            raise ValidationError('This group has already applied for this topic.')
