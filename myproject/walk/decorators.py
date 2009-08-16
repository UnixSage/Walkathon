from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from myproject.walk.models import Person

def walker_required(func):
    def wrapped(request, uuid=None, *args, **kwargs):
        if not request.session.__contains__('walker_uuid'):
            if uuid:
                walker = get_object_or_404(Person, uuid=uuid)
                request.session.__set__('walker_uuid', walker)
            else:
                return HttpResponseRedirect(reverse('walker_not_set'))
        return func(request, *args, **kwargs)
    return wrapped
