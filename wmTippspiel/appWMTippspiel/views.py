from django.http import HttpResponse, HttpResponseRedirect
from wmTippspiel.appWMTippspiel.models import Tipps, Begegnung
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


# Create your views here.
@login_required
def userTipps(request):
    ''' 
    This view shows the usertipps for logged in user 
    '''
    username = request.user.username
    userpk = request.user.pk
    tipps = Tipps.objects.filter(user=userpk)
    
    #tipps = list(tipps)    
    #print tipps
    
    #tipps = list(str(i) for i in tipps)
    
    #liste = ['<li>%s</li>' % i for i in tipps]
    #liste.insert(0, '<ul>')    
    #liste.append('</ul>')    
        
    #tipps = ''.join(liste)

    #print tipps
    #print type(tipps)
    
    #return HttpResponse('<h1>Begegnungen fuer %s</h1> %s' % (username, tipps)) 
    #return HttpResponse('<h1>Tipps von %s </h1> %s' % (username, tipps))
    return render_to_response('appWMTippspiel/usertippsresults.html',
                              {'tipps': tipps, 'username': username})

@login_required
def tippen(request): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    begegnungen = Begegnung.objects.all()
    
    
    
    return render_to_response('appWMTippspiel/tippen.html',
                              {'begegnungen': begegnungen, 'username': username})
    #return HttpResponse('Test')
    
    
def tippenForm(request, begegnungID): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    begegnungen = Begegnung.objects.filter(pk=begegnungID)
    
    print begegnungID 
    
    
    return render_to_response('appWMTippspiel/tippen-form.html',
                              {'begegnungen': begegnungen, 'username': username, 'request': request})
    #return HttpResponse('Test')
    
def tippAusfuehren(request): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    
    myUser = User.objects.get(pk=1)
    myBegegnung = Begegnung.objects.get(pk=1)
    
    ''' Hier das Speichern to do ...'''
    
    tipp = Tipps(user=myUser, begegnung=myBegegnung, toreHeim=2, toreGast=3, tippDatum="2010-05-12 13:00")
    
    print tipp.user
    print tipp.begegnung
    print tipp.toreHeim
    print tipp.toreGast
    print tipp.tippDatum
    
    return HttpResponse('Test')    
    
    
    