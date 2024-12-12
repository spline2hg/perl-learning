from django.urls import path
from . import views
from accounts import views as acc
from django.views.generic import RedirectView

urlpatterns = [
    # path('',views.home_page,name='home'),
    path('',views.gomes_page,name='home'),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    # path('logout/', views.logout_view, name='logout'),
    path('remove_classroom/<int:id>', views.remove_classroom, name='remove_classroom'),
    path('classroom/<int:id>/', views.classroom_detail, name='classroom_detail'),
    # path('classroom/<int:classroom_id>/send_message/', views.send_message, name='send_message'),
    path('edit_classroom/<int:id>/', views.edit_classroom, name='edit_classroom'),
    path('leave_classroom/<int:id>/', views.leave_classroom, name='leave_classroom'),
    path('join_classroom/',views.join_classroom,name='join_classroom'),
    path('joined_classrooms/',views.joined_classrooms,name='joined_classrooms'),
    path('join_classroom/<int:id>',views.join_classroom_wc,name='join_classroom_wc'),
    path('my_classrooms/',views.my_classrooms,name='my_classrooms'),
    path('classrooms_list/',views.classroom_list,name='classroom_list'),
    path('educators/',views.educator_list,name='educator_list'),
    path('try/',acc.tryh,name='try'),
    path('meeting/',views.meeting,name='meeting'),
    path('search/',views.search,name='search'),
    path('classroom_search/',views.classroom_search,name='classroom_search'),
    path('educator_search/',views.educator_search,name='educator_search'),
    path('my_classroom_search/',views.my_classroom_search,name='my_classroom_search'),
    path('create_note/<int:classroom_id>',views.create_note,name='create_note'),
    path('create_alert/<int:classroom_id>',views.create_alert,name='create_alert'),
    path('educator/profile/<int:user_id>/',views.educator_profile,name='educator_profile'),
    path('conversation/<int:edu_user_id>/', views.convo,name='convo'),
    path('conversation/send/<int:edu_user_id>/',views.convo_send,name='convo_send'),
    path('share_url/',views.share_url,name='share_url'),
    path('requests/',views.requests,name='requests'),
    path('create_request/',views.create_request,name='create_request'),
    path('messages/',views.messsage_tab,name='message_tab'),
    path('message/<int:id>', views.messages_tab, name='messages_tab'),
    path('home/',views.gomes_page,name='home_page'),
    path('restricted/',views.restricted,name='restricted'),


]

