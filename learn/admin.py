from django.contrib import admin
from .models import Classroom, Message, Notes,Alerts, PersonalMessage, Requests
# Register your models here.

admin.site.register(Classroom)
admin.site.register(Message)
admin.site.register(Notes)
admin.site.register(Alerts)
admin.site.register(PersonalMessage)
admin.site.register(Requests)
