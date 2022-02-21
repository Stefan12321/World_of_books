from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect


def sign_up(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        print(request.POST)
        print(register_form.errors.values())
        if register_form.is_valid():
            register_form.fields['password'].widget.attrs.update({'class': 'form-control is-valid'})
            register_form.fields['confirm_password'].widget.attrs.update({'class': 'form-control is-valid'})
            register_form.fields['username'].widget.attrs.update({'class': 'form-control is-valid'})
            register_form.fields['email'].widget.attrs.update({'class': 'form-control is-valid'})
            user = User()
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.password = make_password(request.POST.get('password'))
            user.save()
            return HttpResponseRedirect("/accounts/login")
        else:
            if ['Password does not match'] in register_form.errors.values():
                register_form.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
                register_form.fields['confirm_password'].widget.attrs.update({'class': 'form-control is-invalid'})
            if ['This username is already used'] in register_form.errors.values():
                register_form.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            if ['This email is already used'] in register_form.errors.values():
                register_form.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})

    else:
        register_form = RegisterForm()
    return render(request, 'registration/registration.html', {"form": register_form})


def reset_password(request):
    if request.method == "POST":
        print('reset password')
    return render(request, 'registration/reset_password.html')

