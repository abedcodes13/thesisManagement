from django.contrib import admin
from proj_app.models import *

# Register your models here.
myModels = [CustomUser,SupervisorProfile,GroupProfile , Topic, Application, StudentProfile, UnitCoordinatorProfile]
admin.site.register(myModels)