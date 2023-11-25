from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        if phone_number and password:
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return render(request, "auth/login.html")
        return render(request, "auth/login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "auth/register.html")

    def post(self, request):
        return render(request, "auth/register.html")