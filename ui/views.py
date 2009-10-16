from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect

from models import Bugs

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
)

def index_view(request):
    bugs = Bugs.objects.order_by("bug_id").reverse()
    return render_to_response("index.html", {"bugs": bugs})

def bug_view(request, bug_id):
    bug = Bugs.objects.get(bug_id=bug_id)
    comments = bug.longdescs_set.all()
    comments_first = comments[0]
    comments_other = comments[1:]
    return render_to_response("bug.html", {
        "bug": bug,
        "comments_first": comments_first,
        "comments_other": comments_other,
        })

def redirect_index(request):
    return HttpResponseRedirect("ui/")
