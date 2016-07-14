from django.http import HttpResponseRedirect
from django.shortcuts import render
from registration import models
from notification.views import generate_notification_qty_num
from deadline.models import Deadline
from django.contrib import messages
import time, datetime
from sam2017.views import generate_name_role


def __default_context(request, user_identifier):
    user = models.User.objects.get(email=user_identifier)

    context = {
        'show': True,
        'role': user.role.code,
        'num_notification': generate_notification_qty_num(user_identifier),
    }

    return generate_name_role(user, context)


def verify_daily_notifications(request, code):
    prev_date = Deadline.objects.get(type='Notification_deadline')
    today = datetime.date.today()
    update = False
    if prev_date.date < today:
        if code == 'PCC':
            pass
            # update = True
        elif True:
            pass
        else:
            pass

    if update:
        prev_date.date = today
        prev_date.save()


def verify_daily_notifications(request, code):
    prev_date = Deadline.objects.get(type='X')
    today = datetime.date.today()
    update = False

    if prev_date.date < today:
        if code == 'PCC':
            messages.warning(request, "Review for PCC.")
            update = True

        elif True:
            pass

        else:
            pass

    if update:
        prev_date.date = today
        prev_date.save()


def profile(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    verify_daily_notifications(request, models.User.objects.get(email=request.session['user_identifier']).role.code)
    context = __default_context(request, request.session['user_identifier'])

    return render(request, 'user_profile.html', context)
