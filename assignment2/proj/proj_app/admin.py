from django.contrib import admin
from proj_app.models import *

# Register your models here.
myModels = [SupervisorProfile,GroupProfile , Topic, Application]
admin.site.register(myModels)