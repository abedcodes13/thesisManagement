from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm

class UnitCoordinatorForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'unit_coordinator'
        if commit:
            user.save()
            UnitCoordinatorProfile.objects.create(user=user, name=self.cleaned_data['name'], email=self.cleaned_data['email'])
        return user

class SupervisorSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'supervisor'
        if commit:
            user.save()
            SupervisorProfile.objects.create(user=user, name=self.cleaned_data['name'], email=self.cleaned_data['email'])
        return user

class GroupSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'group'
        if commit:
            user.save()
            GroupProfile.objects.create(user=user,
                                         name=self.cleaned_data['name'], 
                                         email=self.cleaned_data['email'])
        return user
    
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    student_id = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'student_id', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(user=user, student_id=self.cleaned_data['student_id'], email=self.cleaned_data['email'])
        return user
    


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topicID', 'title', 'description', 'brief_description', 'category', 'group_limit', 'cas','syd', 'external',
                  'chem_eng', 'cns_eng', 'eee', 'mech_eng', 'cs', 'cyb_sec',
                  'data_sc', 'is_ds', 'seng']
        labels = {
            'brief_description' : 'Brief Description',
            'cas': 'Internal - Casuarina',
            'syd': 'Internal - Sydney',
            'ext': 'External',
            'chem_eng': 'Chemical Engineering',
            'cns_eng': 'Civil and Structural Engineering',
            'eee': 'Electrical and Electronics Engineering',
            'mech_eng': 'Mechanical Engineering',
            'cs': 'Computer Science',
            'cyb_sec': ' Cyber Security',
            'data_sc': 'Data Science',
            'is_ds': 'Information Systems and Data Science',
            'seng': 'Software Engineering',
        }
        widgets = {
            'category': forms.Select(choices=Topic.CATEGORY_CHOICES),
        }



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'email']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['topicID']

    def clean(self):
        cleaned_data = super().clean()
        group = self.instance.groupID
        topic = cleaned_data.get('topicID')
        if group.students.count() < 3 or group.students.count() > 5:
            raise forms.ValidationError('A group must consist of three to five students to apply for a topic.')
        if Application.objects.filter(groupID=group, topicID=topic).exists():
            raise forms.ValidationError('This group has already applied for this topic.')
        return cleaned_data