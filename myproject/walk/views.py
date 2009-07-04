from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from myproject.walk.models import *

def createwalker(request):
    if request.method == 'POST':
        form = WalkerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('http://autismyork.org')
    else:
        form = WalkerForm()
    return render_to_response('createwalker.html', {
        'formset': form,
    })

def walker_private(request, uuid=None, template='walker.html'):
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
            return HttpResponseRedirect(reverse('walker_private', kwargs={'uuid': uuid}))
    else:
        form = SponsorForm()
    return render_to_response(template, {'walker': walker, 'form': form, 'message': message})
