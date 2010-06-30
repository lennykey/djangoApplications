from django.http import HttpResponse, HttpResponseRedirect
from wmTippspiel.appWMTippspiel.models import Tipps, Begegnung, Mannschaft
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from datetime import datetime
from BeautifulSoup import BeautifulSoup

import time
import urllib

#import time
#from wmTippspiel.feedReader.views import feedStart 
import wmTippspiel


# Create your views here.
@login_required
def start(request):
    ''' 
    This view shows the startpage
    '''
    feed = wmTippspiel.feedReader.views.feedStart(request)
    punkteListe = punkteAuswerten(request)
    
    return render_to_response('appWMTippspiel/start.html',
                              {'entries': feed.entries[0:20], 'punkteListe': punkteListe[0:16] })


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
def tippen(request, art=''): 
    ''' 
    This view lists the Begegnungen to the logged in user and makes posible to 
    bet on games
    '''
    
    if art == 'GruppeA':
        art = 'Gruppe A'
    elif art == 'GruppeB':
        art = 'Gruppe B'
    elif art == 'GruppeC':
        art = 'Gruppe C'
    elif art == 'GruppeD':
        art = 'Gruppe D'
    elif art == 'GruppeE':
        art = 'Gruppe E'
    elif art == 'GruppeF':
        art = 'Gruppe F'
    elif art == 'GruppeG':
        art = 'Gruppe G'
    elif art == 'GruppeH':
        art = 'Gruppe H'
    else:
        art = ''
        
    username = request.user.username
    userpk = request.user.pk
    if art == '':
        #tipps = Tipps.objects.filter(user=userpk).order_by('-tippDatum')
        tipps = Tipps.objects.filter(user=userpk).order_by('-begegnung__datum')
        #begegnungen = Begegnung.objects.order_by('tippDatum')
    else:
        tipps = Tipps.objects.filter(user=userpk).order_by('-begegnung__datum')
        #begegnungen = Begegnung.objects.filter(art=art)

    begegnungen = Begegnung.objects.order_by('datum')
    mytipps = [i.begegnung for i in Tipps.objects.filter(user=userpk)]
    
    now = datetime.strptime(datetime.now().isoformat()[0:16],           
                                                  "%Y-%m-%dT%H:%M" )
                                                 
    #now = datetime.now()
    
    begegnungVorbei = Begegnung.objects.filter(datum__lte=now)
    
    
    
    return render_to_response('appWMTippspiel/tippen.html',
                              {'begegnungen': begegnungen, 'username': username,
                               'tipps': tipps, 'begegnungVorbei': begegnungVorbei, 'mytipps': mytipps, 'jetzt':now})
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
    user = User.objects.get(pk=userpk)
    tippDatum = datetime.now()
    
    
    try:
        tipp = Tipps.objects.get(begegnung=begegnung, user=userpk)
    except:
        tipp = Tipps(user=user, begegnung=begegnung, toreHeim=0, toreGast=0,
                     tippDatum=tippDatum.strftime("%Y-%m-%d %H:%M"))
        #tipp.save()
        #tipp = Tipps.objects.get(begegnung=begegnung)
    
    #print begegnungID 
    
    
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
    #print userTipps
    
    jetzt = datetime.now().isoformat()[0:16]
    
    tippDatum = datetime.strptime(jetzt, "%Y-%m-%dT%H:%M")

    toreHeim = request.POST['toreHeim']
    toreGast = request.POST['toreGast']
    
    tipp = Tipps(user=user, begegnung=begegnung, toreHeim=toreHeim,
                  toreGast=toreGast, tippDatum=tippDatum)
    
    begegnungDatumVergleich = datetime.strptime(begegnung.datum.isoformat()[0:16],
                                                 "%Y-%m-%dT%H:%M" )
    jetztDatumVergleich = datetime.strptime(jetzt, "%Y-%m-%dT%H:%M")
    
    #print begegnungDatumVergleich
    #print jetztDatumVergleich
    
    if str(tipp) in userTipps and (jetztDatumVergleich <= begegnungDatumVergleich):
        changeTipp = Tipps.objects.get(user=userpk, begegnung=begegnungID) 
        changeTipp.toreHeim= toreHeim
        changeTipp.toreGast= toreGast
        changeTipp.tippDatum = tippDatum 
        
        changeTipp.save()
        
        message = 'wurde veraendert!'
        
        return HttpResponseRedirect('/wmtippspiel/tippspiel/tippen/')
                              #,
                              #{'begegnung': begegnung, 'toreHeim':toreHeim,
                              #  'toreGast':toreGast, 'user': user, 'message':message})
        #return HttpResponse('Spiel wurde veraendert')
    
    elif str(tipp) not in userTipps and (jetztDatumVergleich <= begegnungDatumVergleich):
        tipp.save()
        
    elif jetztDatumVergleich >= begegnungDatumVergleich:
        message = 'Das Spiel laeuft bereits oder ist bereits aus.' 
        return HttpResponseRedirect('/wmtippspiel/tippspiel/tippen/')
                              #,
                              #{'begegnung': begegnung, 'toreHeim':toreHeim,
                              # 'toreGast':toreGast, 'user': user, 'message': message})
        #return HttpResponse('Das Spiel liegt in der Vergangenheit. Auf das Spiel \
        #                     kann nicht mehr gewettet werden')
    else:
        return HttpResponse('Es ist ein Fehler augetretetn! Jetzt: %s Datum \
                             Begegnung: %s'
                             % (datetime.now().isoformat()[0:16], 
                                begegnung.datum.isoformat()[0:16]))
        
    
    #print "begegnungID: " + begegnungID
    #print user
    #print begegnung
    #print toreHeim
    #print toreGast
    #print tippDatum 
    
    return HttpResponseRedirect('/wmtippspiel/tippspiel/tippen/')
   
    #return render_to_response('appWMTippspiel/tippen.html',
    #                         {'begegnung': begegnung, 'toreHeim':toreHeim,
    #                            'toreGast':toreGast, 'user': user, 'message':message})
    
    #return HttpResponse('Folgender Tipp wurde ausgefuehrt %s Tore: %s : %s vom User: %s' % (begegnung, toreHeim, toreGast, user) )    
    


def punkteAuswerten(request):
    
    #userpk = request.user.pk
    #username = request.user.username
    
    
    #print userpk
    
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
        
        for begegnung in begegnungenAbgelaufen:
            for userTipp in userTipps:
                if userTipp.begegnung == begegnung and begegnung.toreHeim == userTipp.toreHeim and begegnung.toreGast == userTipp.toreGast:
                    #print 'Begegnung %s' % begegnung.pk
                    #print 'Begegnung %s' % begegnung
                    #print 'Begegnung ToreHeim %s ' % begegnung.toreHeim
                    #print 'Begegnung ToreGast %s ' % begegnung.toreGast
                    #print 'UserTipp ToreHeim %s ' % userTipp.toreHeim
                    #print 'UserTipp ToreGast %s ' % userTipp.toreGast
                    punkte += 4
                
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim > begegnung.toreGast and userTipp.toreHeim > userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast == userTipp.toreHeim - userTipp.toreGast):
                    punkte += 2
                    #print 'Begegnung %s' % begegnung.pk
                    #print 'Begegnung %s' % begegnung
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim < begegnung.toreGast and userTipp.toreHeim < userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast == userTipp.toreHeim - userTipp.toreGast):
                    punkte += 2
                    #print 'Begegnung %s' % begegnung.pk
                    #print 'Begegnung %s' % begegnung
                    
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim > begegnung.toreGast and userTipp.toreHeim > userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast != userTipp.toreHeim - userTipp.toreGast):
                    punkte += 1
                    #print 'Begegnung %s' % begegnung.pk
                    #print 'Begegnung %s' % begegnung
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim < begegnung.toreGast and userTipp.toreHeim < userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast != userTipp.toreHeim - userTipp.toreGast):
                    punkte += 1
                    #print 'Begegnung %s' % begegnung.pk
                    #print 'Begegnung %s' % begegnung
                    
                elif userTipp.begegnung == begegnung and (begegnung.toreHeim == begegnung.toreGast and userTipp.toreHeim == userTipp.toreGast) and (begegnung.toreHeim - begegnung.toreGast == userTipp.toreHeim - userTipp.toreGast):
                    punkte += 2
                    
        platzierung = 0
        userPunkte= (aktuellerUsername,punkte,platzierung)
        userPunkteListeAll.append(userPunkte)
    
    userPunkteListeAll = sorted(userPunkteListeAll, key=lambda tipper: tipper[1], reverse=True)
    aktuellerPlatz = 1
    ind = 0
    vorherigePunkte = userPunkteListeAll[0][1]
    for aktuellerUsername, punkte, platzierung in userPunkteListeAll:
        if(int(punkte) < int(vorherigePunkte)):
            aktuellerPlatz += 1
            vorherigePunkte = punkte
            userPunkteListeAll[ind] = (aktuellerUsername, punkte, aktuellerPlatz)
        elif(punkte == userPunkteListeAll[0][1]):
            aktuellerPlatz == 1
            vorherigePunkte = punkte
            userPunkteListeAll[ind] = (aktuellerUsername, punkte, aktuellerPlatz)
        else:
            vorherigePunkte = punkte
            userPunkteListeAll[ind] = (aktuellerUsername, punkte, '*')
        ind += 1
                    
        #print 'Begegnung abgelaufen: %s ' % begegnungenAbgelaufen
    
    #return HttpResponse('Punkte: %s' % (userPunkteListeAll) )
    #return render_to_response('appWMTippspiel/punkte.html', {'userPunkteListeAll':userPunkteListeAll, 'username':username })
    return userPunkteListeAll




def fillMannschaften(request):
    url = 'http://de.fifa.com/worldcup/teams/index.html'
    webpage = urllib.urlopen(url).read()
    
    teams = []
    soup = BeautifulSoup(webpage)
    teamsDiv = soup.find('div', {"class":"tTeamsClean"}).findAll('table')[0]
    teamsTd = teamsDiv.findAll('td')
    
    for i in teamsTd:
        name = str(i.findAll('span')[0].string)
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
            mannschaftHeim = str(g.find('td', {"class":"l homeTeam"}).a.string)
            mannschaftHeimInstance = Mannschaft.objects.get(name=mannschaftHeim)
            
            mannschaftGast = str(g.find('td', {"class":"r awayTeam"}).a.string)
            mannschaftGastInstance = Mannschaft.objects.get(name=mannschaftGast)
            
            datum = g.find('td', {"class":"l dt"}).span.string
            datum = "2010-"+datum[3:5]+"-"+datum[0:2]+" "+datum[6:]+":00"
            art = str(i['summary'])
            
            begegnung= Begegnung(mannschaftHeim=mannschaftHeimInstance, \
                                 mannschaftGast=mannschaftGastInstance, \
                                 datum=datum, \
                                 art=art, toreHeim=0, toreGast=0)
            begegnung.save()
            
            
            games.append((mannschaftHeim, mannschaftGast, datum, art))
    
    return HttpResponse('%s' % games)

def fillNewScores(request):
    url = 'http://de.fifa.com/worldcup/matches/index.html'
    webpage = urllib.urlopen(url).read()
    ldatum = ""
    heimTore, gastTore = 0, 0
    playedGames = []
    soup = BeautifulSoup(webpage)
    groupsT = soup.find('div', {"class":"tGroupDetail"}).findAll('table')
    for i in groupsT:
        groupGames = i.findAll('tr')
        del groupGames[0]
        for g in groupGames:
            heimTore, gastTore = 0, 0
            result = g.contents[5].a.string
            if(result.find(":") != -1):
                if(result.find("(") != -1):
                    result = result[0:result.find(":")+1]+result[result.find(":")+1:result.find("(")-1]
                heimTore = int(result[0:result.find(":")])
                gastTore = int(result[result.find(":")+1:])
                ldatum = g.find('td', {"class":"l dt"}).span.string
                ldatum = "2010-"+ldatum[3:5]+"-"+ldatum[0:2]+" "+ldatum[6:]+":00"
                ldatum = datetime.fromtimestamp(time.mktime(time.strptime(ldatum, "%Y-%m-%d %H:%M:%S")))
                begegnung = Begegnung.objects.get(datum=ldatum)
                begegnung.toreHeim = heimTore
                begegnung.toreGast = gastTore
                begegnung.save()
                playedGames.append((ldatum, heimTore, gastTore))
    return HttpResponse('%s' % playedGames)
    
def points(request):
    punkteListe = punkteAuswerten(request)
    
    return render_to_response('appWMTippspiel/points.html',
                              {'punkteListe': punkteListe})
    
def tippsofbegegnung(request, begegnung=''):
    
    tipps = Tipps.objects.filter(begegnung__id=begegnung)
    
    return render_to_response('appWMTippspiel/tippsofbegegnung.html', {'tipps':tipps})
    
