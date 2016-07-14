from django.shortcuts import render
from registration.models import User
from registration.models import Role
from django.core.urlresolvers import reverse
from . import forms, models
from rate_paper_pcm.models import Paper_PCM_Rate
from deadline.models import Deadline
from notification.views import generate_notification_qty_num
from notification.models import Notifications
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


from sam2017.views import generate_name_role

import datetime

from django.views.decorators.csrf import csrf_exempt


def __default_context(user_identifier):
    context = {
        'show': True,
        'role': models.User.objects.get(email=user_identifier).role.code,
        'num_notification': generate_notification_qty_num(user_identifier),
    }
    return context


def submit(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    user = User.objects.get(email=request.session['user_identifier'])
    context = generate_name_role(user, __default_context(request.session['user_identifier']))
    if Deadline.objects.get(type='Submission_deadline').date < datetime.date.today():
        messages.warning(request, 'Submission deadline is over.')

        return render(request, "user_profile.html", context)
    paper = models.Paper()
    paper.submitter = user
    form = forms.SubmitPaperForm(request.POST or None, request.FILES or None, instance=paper)
    context = __default_context(request.session['user_identifier'])
    context['form'] = form
    context['submit'] = True
    context['btn_title'] = "Submit Paper"

    if request.method == 'POST':
        if form.is_valid():
            paper = form.save()
            submission = models.Submission(paper=paper)
            submission.file = request.FILES['file']
            submission.save()
            try:
                Notifications(
                    sender=user,
                    receiver=models.User.objects.get(role__code='PCC'),
                    message=user.first_name + ' ' + \

                            user.middle_initial + '. ' \
                            + user.last_name + ' submitted paper "' + paper.title + '".',
                ).save()
            except:
                pass

            messages.success(request, "Paper submitted successfully.")
            return HttpResponseRedirect('/paper/my_papers')
    return render(request, "paper/submit_form.html", context)


def choose_paper(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    pcm = User.objects.get(email=request.session['user_identifier'])
    chosen_papers = models.PCMs_Papers.objects.filter(pcm=pcm)
    assigned_papers = models.PCMs_Papers.objects.filter(is_assigned=True)
    papers = models.Paper.objects.exclude(id__in=[x.paper.id for x in chosen_papers]).exclude(submitter=pcm).exclude(
        id__in=[x.paper.id for x in assigned_papers])
    context = __default_context(request.session['user_identifier'])
    context['paper_list'] = papers
    context['choose'] = True
    if request.method == 'POST':
        chosen_papers = request.POST.getlist('papers')
        for c_paper in chosen_papers:
            paper = models.Paper.objects.get(pk=c_paper)
            paper_pcms = models.PCMs_Papers(paper=paper, pcm=pcm)
            paper_pcms.save()
        length = len(chosen_papers)

        if length == 1:
            messages.success(request, 'Paper has been successfully chosen.')
        else:
            messages.success(request, 'Papers have been successfully chosen.')
        return HttpResponseRedirect('choose_paper')

    return render(request, "paper/choose_paper.html", context)

def paper_listing(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    context = generate_name_role(models.User.objects.get(email=request.session['user_identifier']),
                                 __default_context(request.session['user_identifier']))
    user = User.objects.get(email=request.session['user_identifier'])
    if user.role.code == user.role.PCC:
        papers = models.Paper.objects.all()
        context['paper_list'] = papers
    elif user.role.code == user.role.AUT or user.role.code == user.role.PCM:
        papers = models.Paper.objects.filter(submitter=user)
        context['paper_list'] = papers
        context['hide_to_author'] = True
        context['list_papers'] = True
    return render(request, "paper/paper_listing.html", context)

def assign_paper(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    context = generate_name_role(models.User.objects.get(email=request.session['user_identifier']),
                                 __default_context(request.session['user_identifier']))

    context['assign'] = True
    assigned_papers = models.PCMs_Papers.objects.all().filter(is_assigned=True)
    paper = models.Paper.objects.all().exclude(id__in=[x.paper.id for x in assigned_papers])
    context['paper_list'] = paper
    return render(request, 'paper/paper_assignment.html', context)


def assign_pcm(request, paper_id):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    context = generate_name_role(models.User.objects.get(email=request.session['user_identifier']),
                                 __default_context(request.session['user_identifier']))


    selected_paper = models.Paper.objects.get(pk=paper_id)
    paper_pcms = models.PCMs_Papers.objects.all().filter(paper=selected_paper)

    if len(paper_pcms) < 3:
        other_pcms = User.objects.filter(role=2).exclude(id__in=[u.pcm.id for u in paper_pcms])
        number_of_assigned_papers = []

        for u in other_pcms:
            number_of_assigned_papers.append(models.PCMs_Papers.objects.filter(pcm=u, is_assigned=True).count())

        return_val = zip(other_pcms, number_of_assigned_papers)

        context['other_pcms'] = return_val
        context['not_chosen_papers'] = True
    else:
        context['not_chosen_papers'] = False

    context['paper_pcms'] = paper_pcms
    context['assign'] = True
    if request.method == 'POST':
        chosen_pcms = request.POST.getlist('pcms')

        if len(chosen_pcms) != 3:
            context['error_message'] = 'Please assign three PCMs for the selected paper.'
        else:
            selected_paper = models.Paper.objects.get(pk=paper_id)
            for pcm in chosen_pcms:
                user = models.User.objects.get(id=pcm)
                try:
                    paper_pcm = models.PCMs_Papers.objects.get(paper=selected_paper, pcm=user)
                    paper_pcm.is_assigned = True
                    paper_pcm.save()
                except:
                    models.PCMs_Papers.objects.create(paper=selected_paper, pcm=user, is_assigned=True).save()
                Notifications(
                    sender=models.User.objects.get(email=request.session['user_identifier']),
                    receiver=user,
                    message='A paper with the title of ' + selected_paper.title,
                ).save()
            messages.success(request, 'You have successfully assigned paper PCMs.')
            return HttpResponseRedirect('/paper/assign_paper')

    return render(request, 'paper/pcm_assignment.html', context)


def update(request, paper_id):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')

    user = models.User.objects.get(email=request.session['user_identifier'])
    paper = models.Paper.objects.get(pk=paper_id)
    form = forms.UpdatePaperForm(request.POST or None, instance=paper)
    context = __default_context(request.session['user_identifier'])
    context['form'] = form
    context['btn_title'] = "Save Changes"
    context['submit'] = True
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            Notifications(
                sender=user,
                receiver=models.User.objects.get(role__code='PCC'),
                message='A paper with the title of ' + \
                        paper.title + ' has been updated by ' + \
                        user.first_name + ' ' + \
                        user.middle_initial + ' ' + user.last_name,
            ).save()

            Notifications(
                sender=user,
                receiver=models.User.objects.get(role__code='PCC'),
                message='A paper with the title of ' + \
                        paper.title + ' has been updated by ' + \
                        user.first_name + ' ' + \
                        user.middle_initial + ' ' + user.last_name,
            ).save()

            return HttpResponseRedirect('/paper/my_papers')
    return render(request, "paper/submit_form.html", context)


def submissions(request, paper_id):
    if 'user_identifier' not in request.session:
        return JsonResponse({'status_code': 500, 'message': 'An error happened when getting the submissions'})
    try:
        submissions_list = models.Submission.objects.filter(paper_id=paper_id).order_by('-created')
        data = serializers.serialize("json", submissions_list)

        response = {'statusCode': 200, 'message': 'OK', 'data': data, 'media': settings.MEDIA_URL, 'postURL': reverse("paper:submit_file", kwargs={'paper_id': paper_id})}
    except:
        response = {'status_code': 500, 'message': "An error happened when getting the submissions"}
    return JsonResponse(response)


def submit_file(request, paper_id):
    if 'user_identifier' not in request.session:
        return JsonResponse({'status_code': 500, 'message': 'An error happened when submitting'})
    response = {'status_code': 500, 'message': "An error happened when getting the submissions"}
    try:
        if request.method == 'POST':
            paper = models.Paper.objects.get(pk=paper_id)
            submission = models.Submission(paper=paper)
            submission.file = request.FILES['file']
            file_name = str(submission.file.name).lower()
            file_parts = file_name.split(".")
            if not file_parts[-1] in models.Paper.ALLOWED_FORMATS:
                response = {'statusCode': 500, 'message': 'Invalid file format.'}
            else:
                submission.save()
                data = serializers.serialize("json", [submission])
                response = {'statusCode': 200, 'message': 'OK', 'data': data, 'media': settings.MEDIA_URL}
    except:
        pass

    return JsonResponse(response)


@csrf_exempt
def chosen_papers(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    context = __default_context(request.session['user_identifier'])
    if Deadline.objects.get(type='Review_deadline').date < datetime.date.today():
        messages.warning(request, 'Review deadline is over.')
    # print('in chosen-papers')
    logged_in_pcm = models.User.objects.get(email=request.session['user_identifier'])
    chosen_not_assigned = models.PCMs_Papers.objects.filter(pcm=logged_in_pcm, is_assigned=False)
    reviewed_papers = Paper_PCM_Rate.objects.filter(pcm=logged_in_pcm)
    assigned_not_reviewed = models.PCMs_Papers.objects.filter(pcm=logged_in_pcm, is_assigned=True).exclude(
        paper__in=[p.paper for p in reviewed_papers])
    context['chosen_papers'] = chosen_not_assigned
    context['reviewed_papers'] = reviewed_papers
    context['review_paper_pcm'] = True
    context['assigned_not_reviewed'] = assigned_not_reviewed
    return render(request, 'paper/chosen_papers.html', context)


def review_paper(request):
    if 'user_identifier' not in request.session:
        return HttpResponseRedirect('/')
    else:
        context = __default_context(request.session['user_identifier'])
        # assigned_papers = models.PCMs_Papers.objects.all().filter(is_assigned=True)
        max_entries = 3
        review_objects = models.Review.objects.annotate(reviews=Count('paper_id'))[:max_entries]
        reviewed_papers = models.Paper.objects.all().filter(id__in=[aReviewedPaper.paper_id for aReviewedPaper in review_objects])
        context['paper_list'] = reviewed_papers
        return render(request, 'paper/pcm_reviewed_papers.html', context)
