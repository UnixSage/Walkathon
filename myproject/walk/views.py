from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from myproject.walk.models import *
from myproject.walk.paypal import *

def create_walker(request, uuid=None, template='create_walker.html'):
    if request.method == 'POST':
        form = WalkerForm(request.POST)
        if form.is_valid():
            walker=form.save()
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': walker.uuid}))
    else:
        form = WalkerForm()
    return render_to_response(template,
        {
            'formset': form,
        },
        context_instance=RequestContext(request)        
    )

def walker_home(request, uuid=None, template='walker.html'):
    walker = get_object_or_404(Person, uuid=uuid)
    if request.method == 'POST':
        form = WalkerSettingsForm(request.POST, instance=walker)
        if form.is_valid():
            form.save()
    else:
        form = WalkerSettingsForm(instance=walker)
    return render_to_response(template, {'walker': walker, 'form': form}, context_instance=RequestContext(request))
    #return render_to_response(template, {'walker': walker, 'sponsors': sponsors}, context_instance=RequestContext(request))

def walker_edit(request, uuid=None, template='walker_edit.html'):
    walker = get_object_or_404(Person, uuid=uuid)
    if request.method == 'POST':
        form = WalkerSettingsForm(request.POST, instance=walker)
        if form.is_valid():
            form.save()
    else:
        form = WalkerSettingsForm(instance=walker)
    return render_to_response(template, {'walker': walker, 'form': form}, context_instance=RequestContext(request))

def walker_sponsors(request, uuid=None, template='walker_sponsors.html'):
    walker = get_object_or_404(Person, uuid=uuid)
    sponsors = Sponsor.objects.filter(walker=walker)
    return render_to_response(template, {'walker': walker, 'sponsors': sponsors}, context_instance=RequestContext(request))

def walker_add_sponsor(request, uuid=None, template='walker_add_sponsor.html'):
    message = None
    walker = get_object_or_404(Person, uuid=uuid)
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        form.walker = walker
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.walker = walker
            sponsor.save()
            message = 'Successfully added sponsor'
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': uuid}), context_instance=RequestContext(request))
    else:
        form = SponsorForm()
    return render_to_response(template, {'walker': walker, 'form': form, 'message': message}, context_instance=RequestContext(request))

def walker_edit_sponsor(request, uuid=None, id=None, template='walker_edit_sponsor.html'):
    message = None
    # Walker check is pretty much just here for security
    walker = get_object_or_404(Person, uuid=uuid)
    sponsor = get_object_or_404(Sponsor, id=id)
    if request.method == 'POST':
        form = SponsorForm(request.POST, instance=sponsor)
        if form.is_valid():
            form.save()
            message = 'Successfully saved sponsor'
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': uuid}))
    else:
        form = SponsorForm(instance=sponsor)
    return render_to_response(template, {'walker': walker, 'form': form, 'message': message}, context_instance=RequestContext(request))

def walker_delete_sponsor(request, uuid=None):
    message = None
    walker = get_object_or_404(Person, uuid=uuid)
    id = request.POST['sponsor_id']
    sponsor = get_object_or_404(Sponsor, id=id, walker=walker)
    sponsor.delete()
    return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': uuid}))

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

