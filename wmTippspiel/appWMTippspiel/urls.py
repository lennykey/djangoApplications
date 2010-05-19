from django.conf.urls.defaults import *
from wmTippspiel.appWMTippspiel.models import Begegnung, Tipps 
from wmTippspiel.appWMTippspiel.views import userTipps, tippen, tippenForm, tippAusfuehren

info_dict = {
    'queryset': Begegnung.objects.all(),
}


info_dict_tipps = {
    'queryset': Tipps.objects.all(),
}

urlpatterns = patterns('',
    # Generic views muessen z.B. im mein Templateverzeichnis liegen, und ein 
    # Unterverzeichnis muss fuer die jeweilige Applikation erstellt werdern.
    # Falls eine normale View mit Template angelegt wird, muss diese in ein
    # Unterverzeichnis innerhalb der App mit de namen 'templates' gelegt werden. 
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^begegnungen/$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^tipps/$', 'django.views.generic.list_detail.object_list', info_dict_tipps),
    
    (r'^usertipps/$', userTipps),
    (r'^tippen/$', tippen),
    (r'^tippen/tipp-form/(\d+)$', tippenForm),
    (r'^tippen/tipp-form/tippausfuehren$', tippAusfuehren),
   
    #(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
    #  info_dict),
    #url(r'^(?P<object_id>\d+)/results/$',
    #     'django.views.generic.list_detail.object_detail',
    #     dict(info_dict, template_name='polls/results.html'), 'poll_results'),
    #(r'^(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
    
)


