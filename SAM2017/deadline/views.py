from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from . import forms, models
from django.http import HttpResponseRedirect
from registration.models import User


def check_deadline(type):
    pass

# def __default_context(user_identifier):
#     context = {
#         'show': True,
#         'role': User.objects.get(email=user_identifier).role.code
#     }
#     return context
#
#
# def index(request):
#     if 'user_identifier' not in request.session:
#         return HttpResponseRedirect('/')
#
#     deadlines = models.Deadline.objects.all()
#
#     context = __default_context(request.session['user_identifier'])
#
#     context['deadlines'] = deadlines
#
#     context['deadline'] = True
#
#     return render(request, "deadline/index.html", context)
#
#
# def add(request):
#     if 'user_identifier' not in request.session:
#         return HttpResponseRedirect('/')
#
#     form = forms.DeadlineForm(request.POST or None)
#
#     context = __default_context(request.session['user_identifier'])
#
#     context['form'] = form
#
#     context['deadline'] = True
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('deadline:index'))
#
#     return render(request, "deadline/details.html", context)
#
#
# def edit(request, pk):
#     if 'user_identifier' not in request.session:
#         return HttpResponseRedirect('/')
#     context = __default_context(request.session['user_identifier'])
#
#
#     context['deadline'] = True
#
#     if request.method == 'GET':
#         deadline = models.Deadline.objects.get(pk=pk)
#
#         form = forms.DeadlineForm(instance=deadline)
#
#     elif request.method == 'POST':
#         deadline = models.Deadline.objects.get(pk=request.POST['pk'])
#
#         form = forms.DeadlineForm(request.POST, instance=deadline)
#
#         if form.is_valid():
#             form.save()
#
#             return redirect(reverse('deadline:index'))
#
#     return render(request, "deadline/details.html", {'form': form, 'pk': pk})
