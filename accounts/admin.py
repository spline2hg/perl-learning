from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(LearnerProfile)
admin.site.register(EducatorProfile)
admin.site.register(Interest)
admin.site.register(Subject)
# admin.site.register(Classroom)
