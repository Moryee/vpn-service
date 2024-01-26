from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.views.generic import View
from .forms import LoginForm, RegisterForm


class LoginView(View):
    form_class = LoginForm
    template_name = 'auth_templates/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('sites:site-list'))
        else:
            return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('sites:site-list'))
        else:
            return render(request, self.template_name, {'form': form})


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'auth_templates/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('sites:site-list'))
        else:
            return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('sites:site-list'))
        else:
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('auth_templates:login'))
