from django.shortcuts import render, get_object_or_404
from .forms import CreateMeetingForm, MessageForm, Pm_Form, RequestForm
import random
from accounts import models as acc
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import Classroom, Message, Notes,Alerts, PersonalMessage, Requests
from django.db.models import Count
from django.db.models import Q
import environ
from django.contrib.auth.decorators import login_required
from .decorators import only_educator, secure
# Create your views here.



def home_page(request):
    # classroom_codes = Classroom.objects.values_list('room_code', flat=True)
    # for code in classroom_codes:
    #     print(code)
    return render(request,'page_home.html')

@only_educator
@login_required
def create_classroom(request):
    if request.method == 'POST':
        user = request.user
        form = CreateMeetingForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            random_num = random.randint(100000, 999999)
            instance.room_code = random_num
            edu_prof = acc.EducatorProfile.objects.filter(user=user).first()
            instance.educator = edu_prof
            instance.active = True
            instance.save()
            messages.success(request, 'Classroom created successfully!')
            classroom = Classroom.objects.filter(room_code=random_num)
            return redirect(reverse('classroom_detail', args=[instance.id]))
        else:
            messages.error(request, 'Error creating classroom.')

    else:
        form = CreateMeetingForm()

    context = {
        'form':form,
        # 'classroom':classroom
    }


    return render(request,'create_class.html',context)

@secure
@login_required
def edit_classroom(request,id):
    user = request.user
    # current_classsroom = Classroom.objects.filter(id=id)
    current_classroom = get_object_or_404(Classroom, id=id)
    # form = CreateMeetingForm(instance=current_classroom)
    if request.method == 'POST':
        form = CreateMeetingForm(request.POST, instance=current_classroom)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Classroom details edited successfully!')
            return redirect(reverse('classroom_detail', args=[instance.id]))
        else:
            messages.error(request, 'Error creating classroom.')

    else:
        form = CreateMeetingForm(instance=current_classroom)

    context = {
        'form': form,
        'classroom':current_classroom
    }

    return render(request, 'edit_class.html', context)


def remove_classroom(request,id):
    classroom = get_object_or_404(Classroom, id=id)

    if request.method == 'POST':
        classroom = get_object_or_404(Classroom, id=id)
        classroom.delete()
        messages.error(request,'classroom deleted')
        return redirect('create_classroom')

# def classroom_detail(request,id):
#     classroom = get_object_or_404(Classroom, id=id)
#     students = classroom.student.all()
#     learner_profile = request.user.learnerprofile
#     # is_joined = request.user in students
#     # is_joined = students.filter(id=request.user.id).exists()
#     is_joined = classroom.student.filter(id=learner_profile.id).exists()
#     print(students)
#     print(is_joined)
#
#
#
#     context = {
#         'classroom': classroom,
#         'students':students,
#         'is_joined':is_joined
#     }
#     return render(request, 'classroom_details.html', context)

@login_required
def join_classroom(request):
    if request.method == "POST":
        room_code = request.POST['room_code']
        print(room_code)
        classroom = get_object_or_404(Classroom,room_code=room_code)
        if classroom:
            if request.user.user_type == 'learner':
                classroom.student.add(request.user.learnerprofile)
            else:
                classroom.additional_educators.add(request.user.educatorprofile)
            # print('success')
            return redirect(reverse('classroom_detail', args=[classroom.id]))
        else:
            messages.error(request,'error')
    return render(request,'join_classroom.html')

@login_required
def join_classroom_wc(request,id):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom,id=id)
        if classroom:
            # classroom.student.add(request.user.learnerprofile)
            # print('success')

            if request.user.user_type == 'learner':
                classroom.student.add(request.user.learnerprofile)
            else:
                classroom.additional_educators.add(request.user.educatorprofile)
            messages.success(request,'Classroom joined')
        else:
            messages.error(request,'error')
    return redirect(reverse('classroom_detail', args=[id]))

@login_required
def leave_classroom(request,id):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom,id=id )
        classroom.student.remove(request.user.learnerprofile)
        messages.error(request,'Classroom Removed')

    return redirect('classroom_list')

@only_educator
@login_required
def my_classrooms(request):
    user = request.user.educatorprofile

    classrooms = Classroom.objects.filter(educator=user)

    context = {
        'classrooms': classrooms
    }

    for classroom in classrooms:
        print(classroom)
    return render(request,'my_classrooms.html',context)


def classroom_list(request):
    classrooms = Classroom.objects.filter(status='public')

    context = {
        'classrooms': classrooms,
        'query':''
    }
    # classroom_count = classrooms.count()
    # print(classroom_count)
    return render(request,'public_classrooms.html',context)


def educator_list(request):
    educators = acc.EducatorProfile.objects.all()

    context = {
        'educators': educators
    }
    print(educators)
    return render(request,'find_educators.html',context)

@login_required(login_url='login')
def joined_classrooms(request):
    user = request.user.learnerprofile
    j_class = Classroom.objects.filter(student=user)
    print(j_class)

    context = {
        'j_class':j_class
    }
    return render(request,'m_class.html',context)
@login_required
def meeting(request):
    env = environ.Env()
    appID = env('appID')
    serverSecret = env('serverSecret')

    if request.user.is_authenticated:
        name = request.user.full_name
    else:
        name = 'user'

    # print(appID)
    # print(serverSecret)
    context = {
        'appID':appID,
        'serverSecret':serverSecret,
        'name': name
    }
    return render(request,'meeting.html',context)


@login_required
def classroom_detail(request,id):
    is_joined = False
    classroom = get_object_or_404(Classroom, id=id)
    students = classroom.student.all()
    additional_educators = classroom.additional_educators.all()

    if request.user == classroom.educator.user:
        is_joined = True
    print(students)
    notes = Notes.objects.filter(classroom=classroom)
    alerts = Alerts.objects.filter(classroom=classroom)
    if request.user.user_type == 'learner':
        learner_profile = request.user.learnerprofile
        is_joined = classroom.student.filter(id=learner_profile.id).exists()
    elif request.user.user_type == 'educator' and request.user != classroom.educator.user:
        educator_profile = request.user.educatorprofile
        is_joined = classroom.additional_educators.filter(id=educator_profile.id).exists()
        print(is_joined)
    messaage = Message.objects.filter(classroom=classroom)
    print(messaage)

    url = request.POST.get('url')
    print(url)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.classroom = classroom
            message.url = url
            message.save()
            return redirect('classroom_detail', id)

        else:
            messages.error(request,'Error in sending message')


    else:
        form = MessageForm()

    context = {
        'classroom': classroom,
        'students':students,
        'is_joined':is_joined,
        'form':form,
        'cls_messages':messaage,
        'notes':notes,
        'alerts':alerts,
        'additional_educators':additional_educators
    }
    return render(request, 'classroom_details.html', context)


@login_required
def send_message(request,classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.classroom = classroom
            message.save()
            return redirect('classroom_detail', classroom_id)

        else:
            messages.error(request,'Error in sending message')


    else:
        form = MessageForm()

    context = {
        'form':form
    }

    return render(request,'classroom_details.html',context)


@login_required
def search(request,):
    # if request.method == "GET":
    query = request.GET.get('query','')

    context = {
        'query':query
    }

    return render(request,'s.html',context)

def classroom_search(request):
    query = request.GET.get('classroom_query','')
    sort_by = request.GET.get('sort_by','')

    classrooms = Classroom.objects.filter(status='public')

    if query:
        classrooms = classrooms.filter(name__icontains=query)

    if sort_by:
        if sort_by == 'creation_date':
            classrooms = classrooms.order_by('created_at')
        elif sort_by == 'number_of_students':
            classrooms = classrooms.annotate(num_students=Count('student')).filter(num_students__gt=1).order_by('-num_students')
        elif sort_by == 'classroom_name':
            classrooms = classrooms.order_by('name')

    print(classrooms)
    context = {
        'classrooms': classrooms,
        'query':query
    }
    # classroom_count = classrooms.count()
    # print(classroom_count)
    return render(request, 'public_classrooms.html', context)



def my_classroom_search(request):
    query = request.GET.get('classroom_query','')
    sort_by = request.GET.get('sort_by','')

    classrooms = Classroom.objects.filter(educator=request.user.educatorprofile)

    if query:
        classrooms = classrooms.filter(name__icontains=query)

    if sort_by:
        if sort_by == 'creation_date':
            classrooms = classrooms.order_by('created_at')
        elif sort_by == 'number_of_students':
            classrooms = classrooms.annotate(num_students=Count('student')).filter(num_students__gt=1).order_by('-num_students')
        elif sort_by == 'classroom_name':
            classrooms = classrooms.order_by('name')

    # print(classrooms)
    context = {
        'classrooms': classrooms,
        'query':query
    }
    # classroom_count = classrooms.count()
    # print(classroom_count)
    return render(request, 'my_classrooms.html', context)


def educator_search(request):
    query = request.GET.get('educator_query', '')
    sort_by = request.GET.get('sort_by', '')
    print(query)
    educators = acc.EducatorProfile.objects.all()

    if query:
        # educators = educators.filter(user__full_name__icontains=query)
        educators = educators.filter(
            Q(user__full_name__icontains=query) |
            Q(subjects__name__icontains=query)
        ).distinct()

    if sort_by:
        if sort_by == 'creation_date':
            educators = educators.order_by('user__date_joined')
        elif sort_by == 'number_of_students':
            educators = educators.annotate(
                num_students=Count('classrooms__student')
            ).filter(num_students__gt=1).order_by('-num_students')
        elif sort_by == 'classroom_name':
            educators = educators.order_by('user__full_name')
    context = {
        'educators': educators,
        'query': query
    }
    print(educators)
    print(educators.count())
    # classroom_count = classrooms.count()
    # print(classroom_count)
    return render(request, 'find_educators.html', context)

@login_required
def create_note(request,classroom_id):
    classroom = get_object_or_404(Classroom,id=classroom_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Notes.objects.create(content=content,classroom=classroom)
        return redirect('classroom_detail', classroom_id)

@login_required
def create_alert(request,classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Alerts.objects.create(content=content, classroom=classroom)
        return redirect('classroom_detail', classroom_id)



def educator_profile(request,user_id):
    user_profile = acc.CustomUser.objects.get(id=user_id)
    educator_profile = acc.EducatorProfile.objects.get(user=user_profile)

    context = {
        'user': user_profile,
        'educator_profile': educator_profile,
    }

    return render(request, 'educator_profile.html', context)

@login_required
def convo(request,edu_user_id):
    recipient = get_object_or_404(acc.CustomUser, id=edu_user_id)

    if request.method == "POST":
        url = request.POST.get('url')
        print(url)
        form = Pm_Form(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.url = url
            message.save()
            return redirect('convo',edu_user_id)
        else:
            print('gone')
    else:
        form = Pm_Form()


    messages = PersonalMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=recipient)) |
        (Q(sender=recipient) & Q(receiver=request.user))
    ).order_by('created_at')
    context = {
        'per_messages':messages,
        'recipient':recipient,
        'edu_user_id':edu_user_id,
        'form':form
    }
    return render(request,'convo.html',context)

def convo_send(request,edu_user_id):
    recipient = get_object_or_404(acc.CustomUser, id=edu_user_id)

    if request.method == "POST":
        form = Pm_Form(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.save()
            return redirect('convo',edu_user_id)
    else:
        form = Pm_Form()

    context = {
        'form':form,
        'edu_user_id':edu_user_id,
        'recipient':recipient
    }
    return redirect('convo', edu_user_id)


def share_url(request):
    pass


def requests(request):
    user = request.user
    requests = Requests.objects.all()

    print(user)
    context = {
        'requests':requests,
        'user':user
    }



    return render(request,'requests.html',context)


@login_required
def create_request(request):
    # url = request.POST.get('content')
    # print(url)
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            rqst = form.save(commit=False)
            rqst.requester = request.user
            rqst.save()
            messages.success(request,'Request created Successfully')
            return redirect('requests')
        else:
            print('err')

    else:
        form = RequestForm()

    context = {
        'form':form
    }

    return render(request,'create_rqst.html',context)










from django.db.models import Q, Max, Subquery, OuterRef
from django.db.models.functions import Coalesce

def get_message_partners_with_latest_message(user):
    latest_message = PersonalMessage.objects.filter(
        Q(sender=OuterRef('pk'), receiver=user) |
        Q(receiver=OuterRef('pk'), sender=user)
    ).order_by('-created_at')

    return acc.CustomUser.objects.annotate(
        latest_message_time=Coalesce(Subquery(latest_message.values('created_at')[:1]), 'date_joined'),
        latest_message_text=Subquery(latest_message.values('text')[:1])
    ).filter(
        Q(user1_messages__receiver=user) | Q(user2_messages__sender=user)
    ).exclude(id=user.id).distinct().order_by('-latest_message_time')









@login_required
def messsage_tab(request):
    user = request.user
    # per_messages = PersonalMessage.objects.filter(Q(sender=user) | Q(receiver=user))
    message_partners = get_message_partners_with_latest_message(user)

    context = {
        # 'per_messages': per_messages,
        'user':user,
        'per_detail_messages':None,
        'message_partners':message_partners
    }
    # print(per_messages)
    return render(request, 'message_tab.html', context)


@login_required
def messages_tab(request,id):
    user = request.user
    opposite_person = get_object_or_404(acc.CustomUser,id=id)

    # per_messages = PersonalMessage.objects.filter(Q(sender=user) | Q(receiver=user))

    per_detail_messages = PersonalMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=opposite_person)) |
        (Q(sender=opposite_person) & Q(receiver=request.user))
    ).order_by('created_at')


    # per_chan = acc.CustomUser.objects.filter(
    #     Q(user1_messages__receiver=user) | Q(user2_messages__sender=user)
    # ).distinct().exclude(id=user.id)
    # print(per_chan)

    message_partners = get_message_partners_with_latest_message(user)
    # print(message_partners)

    recipient = opposite_person

    if request.method == "POST":
        form = Pm_Form(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.save()
            return redirect('messages_tab', id)
        else:
            print('gone')
    else:
        form = Pm_Form()


    context = {
        # 'per_messages':per_messages,
        'per_detail_messages':per_detail_messages,
        # 'per_chan':per_chan,
        'message_partners':message_partners
    }

    return render(request,'messages_tab.html',context)



def gomes_page(request):
    # educators = acc.EducatorProfile.objects.all()
    #
    # educators = educators.annotate(
    #     num_students=Count('classrooms__student')
    # ).order_by('-num_students')[:4]
    # # print(educators)

    from django.db.models import Count, F

    educators = acc.EducatorProfile.objects.annotate(
        num_students=Count('classrooms__student', distinct=True)
    ).filter(
        num_students__gt=0
    ).order_by('-num_students')[:4]

    context = {
        'educators':educators
    }

    return render(request,'home_page.html',context)


def restricted(request):
    return render(request,'permission_denied.html')