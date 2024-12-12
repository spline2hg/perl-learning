from django.contrib import messages
from django.shortcuts import redirect


def restrict_relogin(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            messages.info(request,"You are already logged in.")
            return redirect('home_page')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func