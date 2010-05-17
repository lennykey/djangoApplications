from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def begegnungen(request):
    return HttpResponse('<h1>Begegnungen</h1>') 