from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

# Create your views here.


class CreateUserView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # save the newly created user
            form.save()

            # authenticate newly created user
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # redirect to home page
            return redirect("landing_page")

        return render(request, "account/register.html", {"form": form})

class LoginView(View):

    def get(self, request):
        
        return render(request, "registration/login.html")




    def post(self, request, *args, **kwargs):

        username = request.POST.get('username', False)
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("landing_page")

        return render(request, "registration/login.html")
