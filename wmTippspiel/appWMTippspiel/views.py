from django.http import HttpResponse, HttpResponseRedirect
from wmTippspiel.appWMTippspiel.models import Tipps, Begegnung, Mannschaft
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import datetime
import urllib
from BeautifulSoup import BeautifulSoup


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
    begegnungen = Begegnung.objects.all().order_by('art')

    tipps = [i.begegnung for i in Tipps.objects.filter(user=userpk)]
    
    
    
    return render_to_response('appWMTippspiel/tippen.html',
                              {'begegnungen': begegnungen, 'username': username,
                               'tipps': tipps})
    #return HttpResponse('Test')
    
@login_required   
def tippenForm(request, begegnungID): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    username = request.user.username
    userpk = request.user.pk
    begegnung = Begegnung.objects.get(id=begegnungID)
    user = User.objects.get(pk=userpk)
    tippDatum = datetime.now()
    
    
    try:
        tipp = Tipps.objects.get(begegnung=begegnung, user=userpk)
    except:
        tipp = Tipps(user=user, begegnung=begegnung, toreHeim=0, toreGast=0,
                     tippDatum=tippDatum.strftime("%Y-%m-%d %H:%M"))
        #tipp.save()
        #tipp = Tipps.objects.get(begegnung=begegnung)
    
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
        return HttpResponse('Das Spiel liegt in der Vergangenheit. Auf das Spiel \
                             kann nicht mehr gewettet werden')
    else:
        return HttpResponse('Es ist ein Fehler augetretetn! Jetzt: %s Datum \
                             Begegnung: %s'
                             % (datetime.now().isoformat()[0:16], 
                                begegnung.datum.isoformat()[0:16]))
        
    
    print "begegnungID: " + begegnungID
    print user
    print begegnung
    print toreHeim
    print toreGast
    print tippDatum 
    
    
    return HttpResponse('Folgender Tipp wurde ausgefuehrt %s Tore: %s : %s vom User: %s' % (begegnung, toreHeim, toreGast, user) )    
    
@login_required
def punkteAuswerten(request):
    
    userpk = request.user.pk
    username = request.user.username
    
    
    print userpk
    
    now = datetime.strptime(datetime.now().isoformat()[0:16],
                                                 "%Y-%m-%dT%H:%M" )
    begegnungenAbgelaufen = Begegnung.objects.filter(datum__lt = now)
    
   
    userPunkteListeAll= []

    alleUser = User.objects.all()

    for aktuellerUser in alleUser:
    
        punkte = 0
        
        aktuellerUsername = aktuellerUser.username
        aktuellerUserpk = aktuellerUser.pk 
        
        userTipps = Tipps.objects.filter(user=aktuellerUserpk)
        print 'Usertipps  %s ' % userTipps
        print 'aktuellerUsername: %s' % aktuellerUsername 
        
        for begegnung in begegnungenAbgelaufen:
            for userTipp in userTipps:
                if userTipp.begegnung == begegnung and begegnung.toreHeim == userTipp.toreHeim and begegnung.toreGast == userTipp.toreHeim:
                    print 'Begegnung %s' % begegnung.pk
                    print 'Begegnung %s' % begegnung
                    print 'Begegnung ToreHeim %s ' % begegnung.toreHeim
                    print 'Begegnung ToreGast %s ' % begegnung.toreGast
                    print 'UserTipp ToreHeim %s ' % userTipp.toreHeim
                    print 'UserTipp ToreGast %s ' % userTipp.toreGast
                    punkte += 3
                
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim > begegnung.toreGast and userTipp.toreHeim > userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast == userTipp.toreHeim - userTipp.toreGast):
                    punkte += 2
                    print 'Begegnung %s' % begegnung.pk
                    print 'Begegnung %s' % begegnung
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim < begegnung.toreGast and userTipp.toreHeim < userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast == userTipp.toreHeim - userTipp.toreGast):
                    punkte += 2
                    print 'Begegnung %s' % begegnung.pk
                    print 'Begegnung %s' % begegnung
                    
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim > begegnung.toreGast and userTipp.toreHeim > userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast != userTipp.toreHeim - userTipp.toreGast):
                    punkte += 1 
                    print 'Begegnung %s' % begegnung.pk
                    print 'Begegnung %s' % begegnung
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim < begegnung.toreGast and userTipp.toreHeim < userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast != userTipp.toreHeim - userTipp.toreGast):
                    punkte += 1
                    print 'Begegnung %s' % begegnung.pk
                    print 'Begegnung %s' % begegnung
                    
        userPunkte= (aktuellerUsername,punkte)
        
        
                  
        userPunkteListeAll.append(userPunkte)
        userPunkteListeAll = sorted(userPunkteListeAll, key=lambda tipper: tipper[1], reverse=True)
                
                    
        print 'Begegnung abgelaufen: %s ' % begegnungenAbgelaufen
    
    #return HttpResponse('Punkte: %s' %  (userPunkteListeAll) )
    return render_to_response('appWMTippspiel/punkte.html', {'userPunkteListeAll':userPunkteListeAll, 'username':username })

def fillMannschaften(request):
    url = 'http://de.fifa.com/worldcup/teams/index.html'
    webpage = urllib.urlopen(url).read()
    
    teams = []
    soup = BeautifulSoup(webpage)
    teamsDiv = soup.find('div', {"class":"tTeamsClean"}).findAll('table')[0]
    teamsTd = teamsDiv.findAll('td')
    
    for i in teamsTd:
        name = i.findAll('span')[0].string
        teams.append(name)

        mannschaft = Mannschaft(name=name)
        mannschaft.save()
        
    
    return HttpResponse('%s' % teams)

def fillBegegnungen(request):
    url = 'http://de.fifa.com/worldcup/matches/index.html'

    webpage = urllib.urlopen(url).read()
    
    games = []
    mannschaftHeim, mannschaftGast, datum, art = "", "", "", ""
    soup = BeautifulSoup(webpage)
    groupsT = soup.find('div', {"class":"tGroupDetail"}).findAll('table')
    for i in groupsT:
        groupGames = i.findAll('tr')
        del groupGames[0]
        for g in groupGames:
            mannschaftHeim = g.find('td', {"class":"l homeTeam"}).a.string
            mannschaftHeimInstance = Mannschaft.objects.get(name=mannschaftHeim) 
            
            mannschaftGast = g.find('td', {"class":"r awayTeam"}).a.string
            mannschaftGastInstance = Mannschaft.objects.get(name=mannschaftGast) 
            
            datum = g.find('td', {"class":"l dt"}).span.string
            datum = "2010-"+datum[3:5]+"-"+datum[0:2]+" "+datum[6:]+":00"
            art = i['summary']
            
            begegnung= Begegnung(mannschaftHeim=mannschaftHeimInstance, \
                                 mannschaftGast=mannschaftGastInstance, \
                                 datum=datum, \
                                 art=art, toreHeim=0, toreGast=0)
            begegnung.save()
            
            
            games.append((mannschaftHeim, mannschaftGast, datum, art))
    
    return HttpResponse('%s' % games)

