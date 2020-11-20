from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper

def organizer_view(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_organizer:
            return view_function(request,*args, **kwargs)
        else:
            return redirect('home')
    return wrapper

def participant_view(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_organizer:
            return redirect('organizer_dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper

def judge_view(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_judge:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('landing_page')
    return wrapper