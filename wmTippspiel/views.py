from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from urllib2 import HTTPRedirectHandler
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
import time

from wmTippspiel.appWMTippspiel.models import Tipps, Begegnung
from wmTippspiel.appWMTippspiel.views import punkteAuswerten


def index(request):

    return HttpResponse('''<h1>Welcome to our super WM Tippspiel</h1>
    <div><a href="displaymeta/">Display Meta Information</a></div>
    <div><a href="time/">What time ist it?</a></div>
    <div><a href="accounts/login/?next=/">Login</a></div>
    <div><a href="accounts/logout/">Logout</a></div>
    <!-- <div><a href="tippspiel/begegnungen/">Alle Begegnungen</a></div> -->
    <!-- <div><a href="tippspiel/tipps/">Tipps</a></div> -->
    <div><a href="tippspiel/usertipps/">Meine Tipps</a></div>
    <div><a href="tippspiel/tippen/">Jetzt tippen</a></div>
    ''')
    


def regist(request):
    if request.method == 'POST':
        error = ''
        if (request.POST['email']=='') or (request.POST['password']=='') or (request.POST['username']==''):
            return render_to_response('appWMTippspiel/falseregister.html', {'error':'Felder nicht komplett ausgefuellt.'})
        
        try:
            user1= User.objects.get(email = request.POST['email'])
        except:
            user1 = None
            error = 'Diese Email oder Username ist schon vergeben.'

        try:
            user2 = User.objects.get(username = request.POST['username'])
        except:
            user2 = None
            error = 'Diese Email oder Username ist schon vergeben.'

        if user1 is None and user2 is None: 
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            user2 = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user2)
            return direct_to_template(request, 'appWMTippspiel/start.html')
        else:
            return render_to_response('appWMTippspiel/falseregister.html', {'error': error})        
    else:
        return render_to_response('appWMTippspiel/falseregister.html', {'error':'Anmeldung fehlgeschlagen.'})



def pwsend(request):
    user = None;
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
        except User.DoesNotExist:
            user = None

    # Template aufrufen
    return render_to_response('appWMTippspiel/pwsend.html', {'user':user})



@login_required(redirect_field_name='next')
def profil(request, player=''):
    jetzt = datetime.strptime(datetime.now().isoformat()[0:16], "%Y-%m-%dT%H:%M" )

    # User-Daten beschaffen
    if (player != '') or (player != None):
        try:
            myUser = User.objects.get(username = player)
        except User.DoesNotExist:
            myUser = request.user
    else:
        myUser = request.user
   

     
    userpk = myUser.pk

    begegnungen = Begegnung.objects.filter(datum__lt=jetzt)
    #tipps = Tipps.objects.filter(user=userpk, begegnung__in=begegnungen).order_by('tippDatum')
    tipps = Tipps.objects.filter(user=userpk, begegnung__in=begegnungen).order_by('begegnung__datum')

    # Highscore holen
    punkteListe = punkteAuswerten(request)


    #tipps2 = []
    #for object in sort(tipps, 'begegnung'):
    #    tipps2.append(object)

    #neueListe = tipps - begegnungen
    #tipps = tipps.filter(tippDatum__lte=jetzt)
    #tipps = filter(tippDatum__lt = jetzt)
    # Template aufrufen
    return render_to_response('appWMTippspiel/profil.html', {'myuser':myUser, 'tipps':tipps, 'jetzt':jetzt, 'player':player, 'punkteListe': punkteListe})


# sort(objects,sortAttrib):
#    nlist = map(lambda object, sortAttrib=sortAttrib: (getattr(object, sortAttrib),object), objects)
#    nlist.sort(reverse=True)
#    return map(lambda (key, object): object, nlist)


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


