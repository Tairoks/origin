from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Registers a new user"""
    if request.method != "POST":
        #Displays an empty form
        form = UserCreationForm()
    else:
        #Processing the completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Login and redirect to home page
            login(request, new_user)
            return redirect('MyApp:index')

    #Display an empty or filled form
    context = {'form': form}
    return render(request, 'registration/register.html', context)

