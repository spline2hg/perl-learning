from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, LearnerProfileForm, EducatorProfileForm  #, CreateMeetingForm
from .models import CustomUser, LearnerProfile, EducatorProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import restrict_relogin
# Create your views here.

def dashboard(request):
    return HttpResponse("Hello, this is a simple HTTP response!")


@restrict_relogin
def login_view(request):
    if request.method == 'POST':
        # print('yes')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email,password=password)
        print(user)
        if user is not None:
            # print('auth')
            login(request,user)
            messages.success(request,'Account login Successfull')

            # next_url = request.GET.get('next')
            # print('g')
            # print(next_url)
            # if next_url:
            #     return redirect(next_url)

            next_url = request.GET.get('next')  # Get the next URL if provided

            print(next_url)
            if next_url:
                print('gg')
                return redirect(next_url)
                print('redirecting')

            return redirect('home')
        else:
            # print('err')
            messages.error(request,'Invalid email or Password')

    return render(request,'login.html')

# @login_required
def logout_view(request):
    if not request.user.is_authenticated :
        messages.info(request,'You are already Logged out')
    else:
        logout(request)
        messages.error(request,'Account Logged out Successfully')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.user_type == 'learner':
                LearnerProfile.objects.create(user=user)
            else:  # educator
                EducatorProfile.objects.create(user=user)

            login(request,user)
            messages.success(request,'Account registered successfully')
            return redirect('login')

        else :
            messages.error(request,'Invalid data')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html',{'form':form })

@login_required
def profile_view(request):
    user = CustomUser.objects.filter(email=request.user.email).first()

    # Initialize both profiles as None
    learner_profile = None
    educator_profile = None

    # Check user type and retrieve corresponding profile
    if user.user_type == 'learner':
        learner_profile = LearnerProfile.objects.filter(user=user).first()
    elif user.user_type == 'educator':
        educator_profile = EducatorProfile.objects.filter(user=user).first()

    context = {
        'user': user,
        'learner_profile': learner_profile,
        'educator_profile': educator_profile,
    }

    return render(request, 'profile_view.html', context)




    # user = CustomUser.objects.filter(email=request.user.email).first()
    # educator = EducatorProfile.objects.filter(id=request.user.id).first()
    #
    # print(user.user_type)
    # print(educator)
    # context = {
    #     'user':user,
    #
    # }
    # return render(request,'profile_view.html',context)

@login_required
def edit_profile(request):
    user = request.user
    if user.user_type == 'learner':
        learner , created = LearnerProfile.objects.get_or_create(user=user)
        form_class = LearnerProfileForm
        print(user.learnerprofile.user)
    elif user.user_type == 'educator':
        educator, created = EducatorProfile.objects.get_or_create(user=user)
        form_class = EducatorProfileForm
    else:
        messages.error(request,'No user type found')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES ,instance=learner if user.user_type == 'learner' else educator)
        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('profile')
        else:
            # print('error')
            messages.error(request,'Invalid Data')

    else:
        form = form_class()

    return render(request,'edit_profile.html',{'form':form})









@login_required
def tryh(request):
    user = request.user
    is_educator = False
    if user.user_type == 'learner':
        learner, created = LearnerProfile.objects.get_or_create(user=user)
        form_class = LearnerProfileForm
        instance = learner
    elif user.user_type == 'educator':
        educator, created = EducatorProfile.objects.get_or_create(user=user)
        form_class = EducatorProfileForm
        instance = educator
        is_educator = True
    else:
        messages.error(request, 'No user type found')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=learner if user.user_type == 'learner' else educator)
        user_change = CustomUserChangeForm(request.POST,instance=user)
        if form.is_valid() and user_change.is_valid():
            form.save()
            user_change.save()
            messages.success(request,'Profile Updated successfully')
            return redirect('profile')
        else:
            # print('error')
            messages.error(request,'Invalid data')
    else:
        form = form_class(instance=instance)
        user_change = CustomUserChangeForm(instance=user)

    context = {
        'form':form,
        'user_change':user_change,
        'is_educator':is_educator
    }

    return render(request, 'try.html', context)




def about(request):
    return render(request,'about.html')









# def create_classroom(request):
#
#     if request.method == 'POST':
#         form = CreateMeetingForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             print('done')
#         else:
#             print('error')
#
#
#     else:
#         form = CreateMeetingForm()
#
#     context = {
#         'form':form
#     }
#
#     return render(request,'create_class.html',context)