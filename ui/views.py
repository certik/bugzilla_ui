from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.views.generic import list_detail

from models import Bugs, Attachments
from bugzilla_ui import settings

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
    (r'^attachment/(\d+)/$', 'attachment_view'),
)

class SearchForm(forms.Form):
    issue_types = forms.ChoiceField(choices=[
        (0, "All issues"),
        (1, "Open issues"),
        ], initial=1)
    search_text = forms.CharField(required=False)

def index_view(request):
    form = SearchForm()
    bugs = Bugs.objects
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search_text"]
            issue_types = int(form.cleaned_data["issue_types"])
            bugs = bugs.filter(short_desc__icontains=search)
            if issue_types == 1:
                bugs = bugs.exclude(bug_status__in=["CLOSED", "RESOLVED"])
    bugs = bugs.order_by("bug_id").reverse()
    return render_to_response("index.html", {
        "bugs": bugs,
        "form": form,
        })

def bug_view(request, bug_id):
    form = SearchForm()
    bug = Bugs.objects.get(bug_id=bug_id)
    comments = bug.longdescs_set.all()
    comments_first = comments[0]
    comments_other = comments[1:]
    attachments = bug.attachments_set.all()
    return render_to_response("bug.html", {
        "bug": bug,
        "comments_first": comments_first,
        "comments_other": comments_other,
        "form": form,
        "attachments": attachments,
        "MEDIA_URL": settings.MEDIA_URL,
        })

def attachment_view(request, attach_id):
    attachment = Attachments.objects.get(attach_id=attach_id)
    data = attachment.attachdata_set.get().thedata
    response = HttpResponse(data)
    response["Content-Disposition"] = "attachment; filename=%s" % \
            attachment.filename
    return response

def redirect_index(request):
    return HttpResponseRedirect("/bugs-ui/")
