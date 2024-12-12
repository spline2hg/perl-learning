from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    # path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_profile/', views.tryh, name='edit_profile'),
    # path('crate_classroom/', views.create_classroom, name='create_classroom'),
    path('about/',views.about,name='about')
]