from django.shortcuts import render
from registration.models import User

from . import models

from sam2017.views import generate_name_role


# ---------------------------------
# generates the notification number
# ---------------------------------
def generate_notification_qty_num(email):
    return models.Notifications.objects.filter(receiver=User.objects.get(email=email)).count()

# end generate_notification_qty_num function


# ------------------------
# returns a common context
# ------------------------
def return_render(request, user):
    context = {
        'show': True,
        'notifications': True,
        'role': user.role.code,
        'notifications_messages': models.Notifications.objects.all().filter(receiver=user),
        'num_notification': generate_notification_qty_num(request.session['user_identifier']),
    }

    context = generate_name_role(user, context) # updates the context

    return render(request, 'notification/notification.html', context)

# end return_render function


# -----------------------------------
# generates the notification template
# -----------------------------------
def notifications(request):
    user = User.objects.get(email=request.session['user_identifier'])

    return return_render(request, user)

# end notifications function


# --------------------------------------
# generates delete_notification function
# --------------------------------------
def delete_notification(request, notification_id):
    models.Notifications.objects.get(id=notification_id).delete()

    user = User.objects.get(email=request.session['user_identifier'])

    return return_render(request, user)

# end delete_notification function
