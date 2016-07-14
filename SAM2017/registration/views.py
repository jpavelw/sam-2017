from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils.utilities import hash_password
from django.contrib import messages

from . import forms, models


# Create your views here.

def register_user(request):
    registration_form = forms.Registration(request.POST or None)

    context = {
        'registration_form': registration_form,
        'link': '/',
        'link_name': 'Return to Login',
    }

    if registration_form.is_valid():
        role = models.Role.objects.get(code='AUT')
        registration_form.set_role(role)
        user = registration_form.save(commit=False)

        user.password = hash_password(user.password)
        user.save()

        request.session['user_identifier'] = registration_form.cleaned_data['email']
        messages.success(request, "You have registered successfully as an author.")

        return HttpResponseRedirect('/user_profile')

    return render(request, 'registration.html', context)
