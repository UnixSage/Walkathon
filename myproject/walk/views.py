from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from myproject.walk.models import *
from myproject.walk.decorators import walker_required
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

def walker_not_set(request):
    return render_to_response('walker_not_set.html', context_instance=RequestContext(request))

def walker_home(request, uuid=None, template='walker.html'):
    walker = get_object_or_404(Person, uuid=uuid)
    if request.method == 'POST':
        form = WalkerSettingsForm(request.POST, instance=walker)
        if form.is_valid():
            form.save()
    else:
        form = WalkerSettingsForm(instance=walker)
    request.session.__setitem__('walker_uuid', uuid)
    return render_to_response(template, {'walker': walker, 'form': form}, context_instance=RequestContext(request))
    #return render_to_response(template, {'walker': walker, 'sponsors': sponsors}, context_instance=RequestContext(request))

def public_home(request, username=None, template='walker.html'):
    walker = get_object_or_404(Person, username=username)
    if request.method == 'POST':
        form = WalkerSettingsForm(request.POST, instance=walker)
        if form.is_valid():
            form.save()
    else:
        form = WalkerSettingsForm(instance=walker)
    return render_to_response(template, {'walker': walker, 'form': form}, context_instance=RequestContext(request))
    #return render_to_response(template, {'walker': walker, 'sponsors': sponsors}, context_instance=RequestContext(request))

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
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': uuid}), context_instance=RequestContext(request))
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
            return HttpResponseRedirect(reverse('walker_home', kwargs={'uuid': uuid}))
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

@walker_required
def test(request):
    #if request.session.__contains__('walker_uuid'):
    #    uuid = request.session.__getitem__('walker_uuid')
    #else:
    #    uuid = None
    walker = _get_walker(request)
    
    return render_to_response('base.html', {'session': walker.uuid}, context_instance=RequestContext(request))
    
def _get_walker(request):
    if request.session.__contains__('walker_uuid'):
        uuid = request.session.__getitem__('walker_uuid')
        walker = get_object_or_404(Person, uuid=uuid)
        return walker
    else:
        return None

    