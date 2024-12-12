from .models import *

classroom_codes = Classroom.objects.values_list('room_code', flat=True)
for code in classroom_codes:
    print(code)