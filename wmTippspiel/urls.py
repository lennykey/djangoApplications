from django.conf.urls.defaults import *
from wmTippspiel.views import index, current_datetime, mylogin, mylogout
from django.contrib import admin





admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index ),    
    (r'^time/$', current_datetime ),
    #(r'^login/$', mylogin ),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # Example:
    # (r'^wmTippspiel/', include('wmTippspiel.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^tippspiel/', include('wmTippspiel.appWMTippspiel.urls')),
    
)
