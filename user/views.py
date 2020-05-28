from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login 

from .forms import RegisterForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})

    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = RegisterForm()

        args = {'form': form}
        return render(request, 'signup.html', args )