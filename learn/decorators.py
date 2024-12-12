from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Classroom

def only_educator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'learner':
            messages.error(request, 'Cannot perform the operation with user type learner')
            return redirect('home_page')

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def secure(view_func):
    def wrapper_func(request,id,*args,**kwargs):
        current_classroom = get_object_or_404(Classroom, id=id)
        if current_classroom.educator.user != request.user:
            messages.error(request,'You are not allowed to perform this ')
            return redirect('restricted')
        else:
            return view_func(request,id,*args,**kwargs)
    return wrapper_func
