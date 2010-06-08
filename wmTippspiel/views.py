from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from urllib2 import HTTPRedirectHandler
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to

from django.shortcuts import render_to_response, get_object_or_404

import datetime



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
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.save()
        user2 = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, user2)
        return direct_to_template(request, 'appWMTippspiel/start.html')
        #return redirect_to('/accounts/profile/', False)
    else:
        return HttpResponseRedirect('Kein Erfolg')



@login_required(redirect_field_name='next')
def profil(request):
    # User-Daten beschaffen
    myUser = request.user

    # Template aufrufen
    return render_to_response('profil.html', {'user':myUser})


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


