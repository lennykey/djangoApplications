from django.conf.urls.defaults import *
from wmTippspiel.appWMTippspiel.models import Begegnung, Tipps 

info_dict = {
    'queryset': Begegnung.objects.all(),
}


info_dict_tipps = {
    'queryset': Tipps.objects.all(),
}
urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^begegnungen/$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^tipps/$', 'django.views.generic.list_detail.object_list', info_dict_tipps),
    
    #(r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
    #  info_dict),
    #url(r'^(?P<object_id>\d+)/results/$',
    #     'django.views.generic.list_detail.object_detail',
    #     dict(info_dict, template_name='polls/results.html'), 'poll_results'),
    #(r'^(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
    
)


