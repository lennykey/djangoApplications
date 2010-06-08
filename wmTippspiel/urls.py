from django.conf import settings
from django.conf.urls.defaults import *
from wmTippspiel.views import index, regist, profil
from wmTippspiel.feedReader.views import feed 
from django.contrib import admin





admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/'}),
    #(r'^$', 'django.contrib.auth.views.login', {'template_name': 'appWMTippspiel/index.html'}),    
    (r'^$', feed),    
    (r'^regist/$', regist),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'appWMTippspiel/falselogin.html'}),
    (r'^profil/$', profil),
    # Example:
    # (r'^wmTippspiel/', include('wmTippspiel.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^tippspiel/', include('wmTippspiel.appWMTippspiel.urls')),
    
)
