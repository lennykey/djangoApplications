# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from mysite.polls.models import Poll, Choice
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

import time


#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    print latest_poll_list
#    print type(latest_poll_list)
#    t = loader.get_template('polls/index.html')
#    c = Context({
#        'latest_poll_list': latest_poll_list,
#    })
#
    #output = ', '.join([' '.join([p.pub_date.strftime('%d/%m/%y'), p.question])
##    return HttpResponse(t.render(c))



#def detail(request, poll_id):
#    try:
#        p = Poll.objects.get(pk=poll_id)
#    except Poll.DoesNotExist:
#        raise Http404
#    return vote() 
    #return render_to_response('polls/detail.html', {'poll': p}, context_instance=RequestContext(request))


#def results(request, poll_id):
#    p = get_object_or_404(Poll, pk=poll_id)
#    return render_to_response('polls/results.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))
#        return HttpResponseRedirect(reverse('mysite.polls.views.results', args=(p.id,)))

