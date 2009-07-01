from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from myproject.walk.models import *

import datetime
def currentDatetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def NewWalker(request):
    if request.method == 'POST':
        form = WalkerForm(request.POST)
        teamform = NewTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('http://autismyork.org')
    else:
        form = WalkerForm()
        teamform = NewTeamForm()
    return render_to_response('NewWalker.html', {
        'formset': form,
        'teamform': teamform,
    })

