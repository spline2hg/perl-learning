from django.shortcuts import render, redirect



def main_home(request):

    return render(request,'main_home.html')