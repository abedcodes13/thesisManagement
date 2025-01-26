from django.shortcuts import render, redirect, get_object_or_404
from proj_app.models import SupervisorProfile, StudentProfile, GroupProfile, Topic, Application
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from proj_app.forms import ApplicationForm, SupervisorSignUpForm, GroupSignUpForm, TopicForm, StudentRegistrationForm, UnitCoordinatorForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


app_name = 'proj_app/'

# Create your views here.

#Views for login, registration

def is_admin(user):
    return user.is_superuser

@login_required
def register_unit_coordinator(request):
    if not request.user.is_superuser or not request.user.is_authenticated:
        return HttpResponseForbidden('no access')

    if request.method == 'POST':
        form = UnitCoordinatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page or any other page after successful registration
    else:
        form = UnitCoordinatorForm()
    return render(request, app_name + '/register_unit_coord.html', {'form': form})

def about(request):
    context={
        'admin_list': create_admins(),
    }
    return render(request, 'proj_app/about.html', context)



def register_supervisor(request):


    if request.method == 'POST':
        form = SupervisorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SupervisorSignUpForm()
    return render(request, app_name + '/register_supervisor.html', {'form': form})


def register_group(request):
    if request.method == 'POST':
        form = GroupSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')  # Redirect to a desired page after registration
    else:
        form = GroupSignUpForm()
    return render(request, app_name + 'register_group.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page or any other page after successful registration
    else:
        form = StudentRegistrationForm()
    return render(request, app_name + 'register_student.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'proj_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    context = {}
    return render(request, app_name + 'home.html', context)


# Views for Topics

@login_required
def add_topic(request):
    if request.user.user_type != 'supervisor':
        return HttpResponseForbidden('You are not authorized to view this page')

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.supervisor = SupervisorProfile.objects.get(user=request.user)
            topic.save()
            return redirect('list_topics')
    else:
        form = TopicForm()
    return render(request, app_name +'add_topic.html', {'form': form})

@login_required
def request_removal(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'supervisor' or topic.supervisor.user != request.user:
        return HttpResponseForbidden('You are not authorized to view this page')

    topic.removal_requested = True
    topic.save()
    return redirect('list_topics')

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    # Ensure the user is a supervisor and is the supervisor of the topic
    if request.user.user_type != 'supervisor' or topic.supervisor.user != request.user:
        return HttpResponseForbidden('You are not authorized to view this page')

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.pending_approval = True
            form.save()
            return redirect('list_topics')
    else:
        form = TopicForm(instance=topic)
    return render(request, app_name + '/edit_topic.html', {'form': form})


def list_topics(request):
    topics = Topic.objects.filter(is_approved=True)
    return render(request, app_name +'topic_list.html', {'topics': topics})


def view_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'proj_app/view_topic.html', {'topic': topic})



@login_required
def list_groups(request):
    groups = GroupProfile.objects.all()
    return render(request, app_name + 'list_groups.html', {'groups': groups})

@login_required
def enroll_in_group(request, group_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden('You are not authorized to view this page')

    group = get_object_or_404(GroupProfile, pk=group_id)
    student = StudentProfile.objects.get(user=request.user)

    if student.group:
        return HttpResponseForbidden("You are already enrolled in a group.")
    if group.students.count() >= 5:
        return HttpResponseForbidden("This group already has 5 students.")
    
    student.group = group
    student.save()
    return redirect('list_groups')


#student





# Unit Coordinator
@login_required
def review_topics(request):
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topics = Topic.objects.filter(is_approved=False, removal_requested=False)
    return render(request, app_name +'review_topics.html', {'topics': topics})

@login_required
def approve_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topic.is_approved = True
    topic.save()
    return redirect('review_topics')

@login_required
def reject_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topic.delete()
    return redirect('review_topics')


@login_required
def list_removal_requests(request):
    if request.user.user_type == 'supervisor':
        topics = Topic.objects.filter(supervisor__user=request.user, removal_requested=True)
    elif request.user.user_type == 'unit_coordinator':
        topics = Topic.objects.filter(removal_requested=True)
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")

    return render(request, app_name + '/list_removal_requests.html', {'topics': topics})

@login_required
def approve_removal(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')
    
    topic.groups.clear()
    topic.applications.all().delete()  # Assuming the related name for applications is `application_set`
    topic.delete()
    return redirect('list_removal_requests')

def reject_removal(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')
    topic.removal_requested = False
    topic.save()
    return redirect('list_removal_requests')


@login_required
def list_pending_topics(request):
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topics = Topic.objects.filter(pending_approval=True)
    return render(request, app_name + '/list_pending_topics.html', {'topics': topics})

@login_required
def approve_topic_changes(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topic.pending_approval = False
    topic.is_approved = True
    topic.save()
    return redirect('list_pending_topics')

@login_required
def reject_topic_changes(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    if request.user.user_type != 'unit_coordinator':
        return HttpResponseForbidden('You are not authorized to view this page')

    topic.pending_approval = False
    topic.save()
    return redirect('list_pending_topics')



#Applications

@login_required
def apply_for_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    student = StudentProfile.objects.get(user=request.user)

    if not student.group:
        return HttpResponseForbidden("You must be enrolled in a group to apply for a topic.")

    group = student.group

    if group.students.count() < 3 or group.students.count() > 5:
        return HttpResponseForbidden("Your group must consist of three to five students to apply for a topic. Please remove existing approved application to apply for another topic.")
    
    # Check if the group has any approved applications
    if Application.objects.filter(groupID=group, status='Approved').exists():
        return HttpResponseForbidden("Your group already has an approved application and cannot apply for more topics.")

    if Application.objects.filter(groupID=group, topicID=topic).exists():
        return HttpResponseForbidden("Your group has already applied for this topic.")
    
    if topic.current_group_count() >= topic.group_limit:
        return HttpResponseForbidden("This topic has reached the maximum number of groups.")

    if request.method == 'POST':
        application = Application(groupID=group, topicID=topic)
        try:
            application.full_clean()
            application.save()
            return redirect('list_topics')  # Redirect to the list of topics
        except ValidationError as e:
            return render(request, app_name + 'apply_for_topic.html', {'errors': e.messages, 'topic': topic})
    
    return render(request, app_name + 'apply_for_topic.html', {'topic': topic})



@login_required
def list_applications(request):
    if request.user.user_type == 'supervisor':
        applications = Application.objects.filter(topicID__supervisor__user=request.user)
    elif request.user.user_type == 'student':
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        if student_profile.group:
            applications = Application.objects.filter(groupID=student_profile.group)
        else:
            applications = []
    elif request.user.user_type == 'unit_coordinator':
        applications = Application.objects.all()
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return render(request, app_name + '/list_applications.html', {'applications': applications})

@login_required
def approve_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.user != application.topicID.supervisor.user:
        return HttpResponseForbidden("You are not authorized to approve this application.")
    
    # Approve the application
    application.status = 'Approved'
    application.supervisor_approval = True
    application.save()

    # Assign the topic to the group
    group = application.groupID
    group.topic = application.topicID
    group.save()


    # Delete all other applications made by this group
    Application.objects.filter(groupID=group).exclude(pk=application.pk).delete()

    return redirect('list_applications')

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.user != application.topicID.supervisor.user:
        return HttpResponseForbidden("You are not authorized to reject this application.")
    application.status = 'Rejected'
    application.supervisor_approval = True
    application.save()
    return redirect('list_applications')
    
@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if request.user.user_type == 'student':
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        if application.groupID != student_profile.group:
            return HttpResponseForbidden("You are not authorized to delete this application.")
    else:
        return HttpResponseForbidden("You are not authorized to delete this application.")

    if request.method == 'POST':
        application.delete()
        return redirect('list_applications')
    
    return render(request, app_name + '/confirm_delete_application.html', {'application': application})




def create_admins():
    admin_list=[]
    admin_list.append(Admin(361222,
                            'Muhammed Abed'))
    admin_list.append(Admin(365145,
                            'Heshara Danathma Balasooriya Balasooriya Mudiyanselage'))    
    return admin_list


# Define Admin class
class Admin:
    def __init__(self, id, name):
        self.id = id
        self.name= name

    
    def __str__(self):
        return str(self.id) +", " + self.name
    

#kept for future work
@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    
    # Ensure the user is a supervisor and is the supervisor of the topic
    if request.user.user_type != 'supervisor' or topic.supervisor.user != request.user:
        return HttpResponseForbidden('You are not authorized to view this page')

    if request.method == 'POST':
        topic.delete()
        return redirect('list_topics')
    return render(request, app_name + '/confirm_delete.html', {'topic': topic})