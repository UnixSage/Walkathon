from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from walk.models import *
from walk.decorators import walker_required
from walk.paypal import *

def create_walker(request, uuid=None, template='create_walker.html'):
    if request.method == 'POST':
        form = WalkerForm(request.POST)
        if form.is_valid():
            walker=form.save()
            mail_template = loader.get_template('email/welcome.txt')
            context = Context({'username': walker.username, 'uuid': walker.uuid})
            mail_body = mail_template.render(context)
            send_mail(settings.EMAIL_WELCOME_SUBJECT, mail_body, 'walk@autismyork.org', [walker.email], fail_silently=False)
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': walker.uuid}))
    else:
        form = WalkerForm()
    return render_to_response(template,
        {
            'formset': form,
        },
        context_instance=RequestContext(request)        
    )

def walker_not_set(request):
    return render_to_response('walker_not_set.html', context_instance=RequestContext(request))

def walker_home(request, uuid=None, template='walker.html'):
    try:
        announcements = FlatPage.objects.get(url='walker_announcements')
    except ObjectDoesNotExist:
        announcements = None
    walker = get_object_or_404(Person, uuid=uuid)
    request.session.__setitem__('walker_uuid', walker.uuid)
    current_pledges = Sponsor.objects.filter(walker=walker).aggregate(Sum('amount'))['amount__sum']
    current_sponsors = Sponsor.objects.filter(walker=walker).aggregate(Count('amount'))['amount__count']
    current_collected = Sponsor.objects.filter(walker=walker, paid=True).aggregate(Sum('amount'))['amount__sum']
    return render_to_response(template, {
        'walker': walker, 
        'announcements': announcements,
        'current_pledges': current_pledges,
        'current_sponsors': current_sponsors,
        'current_collected': current_collected
    }, context_instance=RequestContext(request))

def public_home(request, username=None, template='walker_public.html'):
    walker = get_object_or_404(Person, username=username)
    current_pledges = Sponsor.objects.filter(walker=walker).aggregate(Sum('amount'))['amount__sum']
    current_sponsors = Sponsor.objects.filter(walker=walker).aggregate(Count('amount'))['amount__count']
    return render_to_response(template, {
        'walker': walker, 
        'current_pledges': current_pledges,
        'current_sponsors': current_sponsors,
    }, context_instance=RequestContext(request))

@walker_required
def walker_example(request, uuid=None, template='walker_email_templates.html'):
    walker = _get_walker(request)
    current_pledges = Sponsor.objects.filter(walker=walker).aggregate(Sum('amount'))['amount__sum']
    current_sponsors = Sponsor.objects.filter(walker=walker).aggregate(Count('amount'))['amount__count']
    return render_to_response(template, {
        'walker': walker, 
        'current_pledges': current_pledges,
        'current_sponsors': current_sponsors,
    }, context_instance=RequestContext(request))

@walker_required
def walker_edit(request, template='walker_edit.html'):
    walker = _get_walker(request)
    if request.method == 'POST':
        form = WalkerSettingsForm(request.POST, instance=walker)
        if form.is_valid():
            form.save()
    else:
        form = WalkerSettingsForm(instance=walker)
    return render_to_response(template, {'walker': walker, 'form': form}, context_instance=RequestContext(request))

@walker_required
def walker_sponsors(request, template='walker_sponsors.html'):
    walker = _get_walker(request)
    sponsors = Sponsor.objects.filter(walker=walker)
    return render_to_response(template, {'walker': walker, 'sponsors': sponsors}, context_instance=RequestContext(request))

@walker_required
def walker_add_sponsor(request, template='walker_add_sponsor.html'):
    message = None
    walker = _get_walker(request)
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        form.walker = walker
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.walker = walker
            sponsor.save()
            message = 'Successfully added sponsor'
            return HttpResponseRedirect(reverse('walker_sponsors'))
    else:
        form = SponsorForm()
    return render_to_response(template, {'walker': walker, 'form': form, 'message': message}, context_instance=RequestContext(request))

@walker_required
def walker_edit_sponsor(request, id=None, template='walker_edit_sponsor.html'):
    message = None
    # Walker check is pretty much just here for security
    walker = _get_walker(request)
    sponsor = get_object_or_404(Sponsor, id=id)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            message = 'Successfully saved sponsor'
            return HttpResponseRedirect(reverse('walker_sponsors'))
    else:
        form = SponsorForm(instance=sponsor)
    return render_to_response(template, {'walker': walker, 'form': form, 'message': message}, context_instance=RequestContext(request))

@walker_required
def walker_delete_sponsor(request):
    message = None
    walker = _get_walker(request)
    id = request.POST['sponsor_id']
    sponsor = get_object_or_404(Sponsor, id=id, walker=walker)
    sponsor.delete()
    return HttpResponseRedirect(reverse('walker_sponsors'))

@walker_required
def walker_team(request, template='teams/walker_team.html'):
    walker = Person.objects.get(id=_get_walker(request).id)
    if request.method == 'POST':
         team = request.POST.get('team')
         if team and team != '0':
             walker.team = Team.objects.get(id=team)
             walker.save()
         return HttpResponseRedirect(reverse('walker_team'))
    teams = Team.objects.all()
    return render_to_response(template, {'walker': walker, 'teams': teams}, context_instance=RequestContext(request))

@walker_required
def create_team(request, template='teams/create_team.html'):
    walker = _get_walker(request)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            walker.team = team
            walker.is_captain = True
            walker.save()
            return HttpResponseRedirect(reverse('walker_team'))
    else:
        form = TeamForm()
    return render_to_response(template,
        {
            'form': form,
        },
        context_instance=RequestContext(request)        
    )

@walker_required
def teams(request, template='teams/teams.html'):
    walker = _get_walker(request)
    teams = Team.objects.all()
    return render_to_response(template, {'walker': walker, 'teams': teams}, context_instance=RequestContext(request))

@walker_required
def team_roster(request, template='teams/roster.html'):
    walker = _get_walker(request)
    persons = Person.objects.filter(team=walker.team)
    return render_to_response(template, {
        'walker': walker,
        'persons': persons
    }, context_instance=RequestContext(request))

@walker_required
def team_fullroster(request, template='teams/fullroster.html'):
    walker = _get_walker(request)
    if walker.is_staff==0:
        return HttpResponse('<a href="/">Error - Click to return Home</a>')
    persons = Person.objects.order_by('team')
    return render_to_response(template, {
        'walker': walker,
        'persons': persons
    }, context_instance=RequestContext(request))

@walker_required
def team_captroster(request, template='teams/captroster.html'):
    walker = _get_walker(request)
    if walker.is_staff==0:
        return HttpResponse('<a href="/">Error - Click to return Home</a>')
    persons = Person.objects.filter(is_captain=1).order_by('team')
    return render_to_response(template, {
        'walker': walker,
        'persons': persons
    }, context_instance=RequestContext(request))

class MyEndPoint(Endpoint):
    def process(self, data):
        datatest=1
        # Do something with valid data from PayPal - e-mail it to yourself,
        # stick it in a database, generate a license key and e-mail it to the
        # user... whatever
        
    def process_invalid(self, data):
        datatest=1
        # Do something with invalid data (could be from anywhere) - you 
        # should probably log this somewhere

    
def _get_walker(request):
    if request.session.__contains__('walker_uuid'):
        uuid = request.session.__getitem__('walker_uuid')
        walker = get_object_or_404(Person, uuid=uuid)
        return walker
    else:
        return None

def stats(request, template='global_stats.html'):
    current_pledges = Sponsor.objects.aggregate(Sum('amount'))['amount__sum']
    current_sponsors = Sponsor.objects.aggregate(Count('amount'))['amount__count']
    current_walkers = Person.objects.aggregate(Count('username'))['username__count']
    current_teams = Team.objects.aggregate(Count('name'))['name__count']
    current_collected = Sponsor.objects.aggregate(Sum('amount'))['amount__sum']
    return render_to_response(template, {
        'current_pledges': current_pledges,
        'current_sponsors': current_sponsors,
        'current_walkers': current_walkers,
        'current_teams': current_teams,
        'current_collected': current_collected
    }, context_instance=RequestContext(request))
