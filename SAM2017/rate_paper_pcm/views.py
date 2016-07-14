from paper.models import PCMs_Papers, Paper
from registration.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from notification.views import generate_notification_qty_num
from . import forms
from .models import Paper_PCM_Rate
from notification.models import Notifications
from sam2017.views import generate_name_role

def default_context(request):
    user = User.objects.get(email=request.session['user_identifier'])
    context = {
        'role': user.role.code,
        'show': True,
        'num_notification': generate_notification_qty_num(request.session['user_identifier']),
    }

    return context


def rate_paper_pcm(request):
    user = User.objects.get(email=request.session['user_identifier'])

    assigned_papers = PCMs_Papers.objects.all().filter(pcm=user, is_assigned=True)
    rated_papers = Paper_PCM_Rate.objects.all().filter(pcm=user)

    my_assigned_papers = []

    found = False

    for element in assigned_papers:
        for rp in rated_papers:
            if rp.paper.title == element.paper.title:
                found = True

        if not found:
            my_assigned_papers.append(element.paper)
        else:
            found = False

    return render(request, "rate_paper_pcm/rate_paper.html", {
        'show': True,
        'role': user.role.code,
        'ap': my_assigned_papers,
        'num_notification': generate_notification_qty_num(request.session['user_identifier']),
    })


def rate_paper_pcm_input_form(request, paper_id):
    paper = Paper.objects.get(id=paper_id)

    review_form = forms.ReviewForm(request.POST or None)

    user = User.objects.get(email=request.session['user_identifier'])

    context = {
        'paper': paper,
        'review_form': review_form,
        'review_paper_pcm': True,
        'role': user.role.code,
        'show': True,
        'num_notification': generate_notification_qty_num(request.session['user_identifier']),
    }

    if review_form.is_valid():
        review_form.set_paper(paper)
        review_form.set_pcm(User.objects.get(email=request.session['user_identifier']))
        review_form.set_decision(review_form.cleaned_data['final_decision'])

        review_form.save()

        if Paper_PCM_Rate.objects.filter(paper=paper).count() == 3:
            Notifications(
                sender=user,
                receiver=User.objects.get(role__code='PCC'),
                message=paper.title + ' completed all its reviews.'
            ).save()

        messages.success(request, "Review submitted.")

        return HttpResponseRedirect('/paper/chosen_papers')

    return render(request, "rate_paper_pcm/rate_paper_input_form.html", context)


def pcc_rate_paper(request, paper_id):
    context_instance = default_context(request)

    form = forms.FinalRatingForm()
    user = User.objects.get(email=request.session['user_identifier'])

    paper_obj = Paper.objects.get(id=paper_id)

    paper_reviews = Paper_PCM_Rate.objects.filter(paper=paper_obj)

    if request.method == 'POST':
        form = forms.FinalRatingForm(request.POST)
        if request.POST['form-type'] == "issue_form":
            for r in paper_reviews:
                r.has_conflict = True
                r.save()
            paper_obj.has_conflict = True
            paper_obj.save()
            messages.success(request, 'Paper conflict has successfully been issued.')
            return HttpResponseRedirect('/rate_paper_pcm/reviewed_papers/')
        else:
            if form.is_valid():
                # print('issue conflict form')
                messages.success(request, 'Paper has been successfuly rated.')
                val = form.data['final_decision']
                # print(val)
                paper_obj.final_rating = val
                paper_obj.save()
                for i in paper_reviews:
                    Notifications(
                        sender=user,
                        receiver=i.pcm,
                        message=paper_obj.title + ' has been rated by PCC.'
                     ).save()
                return HttpResponseRedirect('/rate_paper_pcm/reviewed_papers/')
    context_instance['form'] = form
    context_instance['paper_reviews'] = paper_reviews
    context_instance['paper_author'] = paper_obj.submitter.first_name
    context_instance['paper_title'] = paper_obj.title
    return render(request, 'paper/rate_paper_pcc/pcc_rate_paper.html', context_instance)


def reviewed_papers(request):
    user = User.objects.get(email=request.session['user_identifier'])
    context_instance = generate_name_role(user, default_context(request))
    context_instance = default_context(request)
    context_instance['reviewed'] = True
    user = User.objects.get(email=request.session['user_identifier'])
    distinct_reviewed_papers = Paper_PCM_Rate.objects.values('paper').annotate(reviews=Count('review')).order_by()
    paper_id = []
    review_count = []
    for res in distinct_reviewed_papers:
        paper_id.append(res.get('paper'))
        review_count.append(res.get('reviews'))
    papers = Paper.objects.filter(id__in=[i for i in paper_id])
    not_reviewed_papers = Paper.objects.exclude(id__in=[x for x in paper_id])
    print(not_reviewed_papers)
    reviewed_papers = zip(papers, review_count)
    context_instance['reviewed_papers'] = reviewed_papers
    context_instance['not_reviewed_papers'] = not_reviewed_papers
    return render(request, 'paper/rate_paper_pcc/reviewed_papers_list.html', context_instance)

def resolve_paper_conflict(request, paper_id):
    context_instance = default_context(request)
    paper_obj = Paper.objects.get(id=paper_id)
    user = User.objects.get(email=request.session['user_identifier'])
    paper_reviews = Paper_PCM_Rate.objects.filter(paper=paper_id)
    other_reviews = paper_reviews.exclude(pcm=user)
    user_review = paper_reviews.filter(pcm=user)
    user_review_obj = user_review[0]
    review = user_review[0].review
    decision = user_review[0].decision
    context_instance['reviewed'] = True
    review_form = forms.ReviewForm(request.POST or None, initial={'review': review, 'final_decision': decision})
    if request.method == 'POST':
        if review_form.is_valid():
            messages.success(request, 'Review has been successfully submited. Please wait for final rating of PCC.')
            counter = 0
            for i in other_reviews:
                print(i.has_conflict)
                if i.has_conflict == 1:
                    counter = counter + 1
            print(counter)
            if counter == 0:
                paper_obj.has_conflict = False
                paper_obj.save()
                Notifications(
                    sender=user,
                    receiver=User.objects.get(role__code='PCC'),
                    message=paper_obj.title + ' has all the reviews re-submitted.Conflict has been resolved.'
                ).save()
            user_review_obj.decision = review_form.data['final_decision']
            user_review_obj.review = review_form.data['review']
            user_review_obj.has_conflict = False
            user_review_obj.save()
            return HttpResponseRedirect('/paper/chosen_papers')
    context_instance['review_form'] = review_form
    context_instance['paper_reviews'] = other_reviews
    context_instance['paper_title'] = paper_obj.title
    return render(request, 'paper/rate_paper_pcc/resolve_conflict.html', context_instance)
