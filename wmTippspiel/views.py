from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from urllib2 import HTTPRedirectHandler
from django.contrib.auth.decorators import login_required

import datetime



def index(request):
    '''
     Log in the raw way! Besser decorator fuer das LogIn verwenden
     @login_required(redirect_field_name='next') 
    '''
    #if request.user.is_authenticated():
    #    return HttpResponse('Is Authenticated <a href="logout/">Logout</a>') 
    #  
    #else:
    #    return HttpResponse('''
    #        Login:
    #        
    #        <form method="POST" action="login/">
    #        <input type="text" name="username"></input>
    #        <input type="text" name="password"></input>
    #        <input type="submit" value="Submit"></input>
    #        </form>
    #    
    #    ''')
    
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
    
    #assert False
    

def mylogin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
          if user.is_active:
            login(request, user)
            # success
            return HttpResponse('Login geschafft <a href="/">Home</a>')
          else:
            # disabled account
            return direct_to_template(request, 'inactive_account.html')
        else:
          # invalid login
          return HttpResponse('Invalid Login') 
    else:
          return HttpResponse('Kein Post') 
  
def mylogout(request):
    if request.user.is_authenticated():
        logout(request)
    
    return HttpResponseRedirect('/')


@login_required(redirect_field_name='next')
def current_datetime(request):
    '''
    Diese Methode ist nur fuer Logged-In User sichtbar. Der standard Redirect
    Name der Variable in der Url ist "next". wenn es gewuenscht wird, kann dies
    im @login_required(redirect_field_name='next') Decorator geandert werden. 
    Beispiel:
        @login_required(redirect_field_name='weiterleitenZu')
        
        Wenn die Variable "next" heissen soll, dann kann auch nur
        "@login_required" mit oder ohne Klammern vor der zu schuetzenden View
        gesetzt werden.
    '''
    
    now = datetime.datetime.now()
    
    myUser = request.user
    
    html = "<html><body>It is now %s. Username: %s</body></html>" % (now, myUser.username)
    
    return HttpResponse(html)


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


