from pamela.models import Mac, MacForm
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
from django.shortcuts import get_object_or_404
import json, datetime


def show_macs(request):
    ''' Function used to show the mac address 
    of the people who are present.
    Returns a httpresponse in json {"color": ["user"]}'''
    macs = Mac.objects.all().filter(last_seen__gte=datetime.datetime.today()-datetime.timedelta(minutes=5))
    j = []
    for mac in macs:
        public = mac.mac
        if mac.owner:
            public = mac.owner
            if mac.machine:
                public += " ({})".format(mac.machine)
        j.append(public)
    return HttpResponse(json.dumps(j), content_type="application/json")

def update_macs(newmacs):
    ''' If a new mac address is detected,
    store it in the db '''
    for mac in newmacs:
        item, new= Mac.objects.get_or_create(mac=mac)
        if new: print('New mac detected')
        item.ip = newmacs[mac]
        item.save()

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def set(request):
    ''' Set the owner-machine data if the form and the
    http method are correct.
    Returns a httpresponse '''
    if request.method == 'POST':
        form = MacForm(request.POST)
        if form.is_valid():
            item = get_object_or_404(Mac,ip=request.META.get('REMOTE_ADDR'))
            if form.cleaned_data['owner']:
                item.owner = form.cleaned_data['owner']
            if form.cleaned_data['machine']:
                item.machine = form.cleaned_data['machine']
            item.save()
            return HttpResponse('OK')
        else:
            return HttpResponse('Bad form')
    else:
        return HttpResponse('Bad method')

def get(request):
    ''' Return the owner name and his mac address 
    in a dict {'owner':'user', 'machine':'00:00:...'}'''
    item = get_object_or_404(Mac,ip=request.META.get('REMOTE_ADDR'))
    response = {
        'owner':item.owner,
        'machine':item.machine
    }
    return HttpResponse(json.dumps(response), content_type="application/json") # Redirect after POST
