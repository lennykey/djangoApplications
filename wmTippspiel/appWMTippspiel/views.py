from django.http import HttpResponse, HttpResponseRedirect
from wmTippspiel.appWMTippspiel.models import Tipps, Begegnung
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import datetime


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
    
@login_required   
def tippenForm(request, begegnungID): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    begegnung = Begegnung.objects.get(pk=begegnungID)
    
    tipp = Tipps.objects.get(begegnung=begegnung)
    
    print begegnungID 
    
    
    return render_to_response('appWMTippspiel/tippen-form.html',
                              {'begegnung': begegnung, 'username': username, 
                               'request': request, 'tipp': tipp})
    #return HttpResponse('Test')
@login_required    
def tippAusfuehren(request): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    
    begegnungID= request.POST['begegnungID']
    
    user = User.objects.get(pk=userpk)
    begegnung = Begegnung.objects.get(pk=begegnungID)
    userTipps = Tipps.objects.filter(user=user.pk)
    userTipps = list(str(i) for i in userTipps)
    print userTipps
    
    jetzt = datetime.now().isoformat()[0:16]
    
    tippDatum = datetime.strptime(jetzt, "%Y-%m-%dT%H:%M")

    toreHeim = request.POST['toreHeim']
    toreGast = request.POST['toreGast']
    
    tipp = Tipps(user=user, begegnung=begegnung, toreHeim=toreHeim,
                  toreGast=toreGast, tippDatum=tippDatum)
    
    begegnungDatumVergleich = datetime.strptime(begegnung.datum.isoformat()[0:16],
                                                 "%Y-%m-%dT%H:%M" )
    jetztDatumVergleich = datetime.strptime(jetzt, "%Y-%m-%dT%H:%M")
    
    print begegnungDatumVergleich
    print jetztDatumVergleich
    
    if str(tipp) in userTipps and (jetztDatumVergleich <= begegnungDatumVergleich):
        changeTipp = Tipps.objects.get(user=userpk, begegnung=begegnungID) 
        changeTipp.toreHeim= toreHeim
        changeTipp.toreGast= toreGast
        changeTipp.tippDatum = tippDatum 
        
        changeTipp.save()
        
        return HttpResponse('Spiel wurde veraendert')
    
    elif str(tipp) not in userTipps and (jetztDatumVergleich <= begegnungDatumVergleich):
        tipp.save()
        
    elif jetztDatumVergleich >= begegnungDatumVergleich: 
        return HttpResponse('Das Spiel liegt in der Vergangenheit')
    else:
        return HttpResponse('Es ist ein Fehler augetretetn! Jetzt: %s Datum Begegnung: %s'
                             % (datetime.now().isoformat()[0:16], begegnung.datum.isoformat()[0:16]))
        
    
    print "begegnungID: " + begegnungID
    print user
    print begegnung
    print toreHeim
    print toreGast
    print tippDatum 
    
    
    return HttpResponse('Folgender Tipp wurde ausgefuehrt %s Tore: %s : %s vom User: %s' % (begegnung, toreHeim, toreGast, user) )    
    
    
    