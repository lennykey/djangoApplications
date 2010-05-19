from django.http import HttpResponse, HttpResponseRedirect
from wmTippspiel.appWMTippspiel.models import Tipps 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.
@login_required
def userTipps(request):
    ''' 
    These view shows the tipps user have done
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
 