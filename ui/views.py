from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$',      'index_view'),
)

def index_view(request):
    return render_to_response("index.html")

def redirect_index(request):
    return HttpResponseRedirect("ui/")
