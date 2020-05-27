from django.shortcuts import render, redirect

from .forms import RegisterForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home/') 
    else:
        form = RegisterForm()

        args = {'form': form}
        return render(request, 'signup.html', args )