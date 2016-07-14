from django.http import HttpResponseRedirect
from django.shortcuts import render
from registration import forms
from registration import models
from utils.utilities import check_password
from django.contrib import messages


def index(request):
    login_form = forms.Login(request.POST or None)

    context = {
        'login_form': login_form,
        'show': False,
        'link_name': 'Sign Up',
        'link': '/register'
    }

    if request.method == 'POST':
        if login_form.is_valid():  # add a try catch method here.
            try:
                user = models.User.objects.get(email=login_form.cleaned_data['email'])
                if check_password(user.password, login_form.cleaned_data['password']):
                    request.session['user_identifier'] = user.email
                    return HttpResponseRedirect("/user_profile")
                else:
                    messages.error(request, "Invalid email or password.")

            except:
                messages.error(request, "Invalid email or password.")

    return render(request, 'home.html', context)


# -----------------------------------------------------------------
# centralize the generation of the top name and role for every page
# -----------------------------------------------------------------
def generate_name_role(user, context):
    context['name'] = user.first_name + ' ' \
                      + user.middle_initial + '. ' \
                      + user.last_name

    context['user_role'] = user.role.code

    return context


def logout_user(request):
    del request.session['user_identifier']
    return HttpResponseRedirect("/")
