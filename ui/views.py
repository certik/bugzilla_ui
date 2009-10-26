from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.views.generic import list_detail

from models import Bugs, Attachments, Profiles
from bugzilla_ui import settings

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
    (r'^u/(\S+)/$', 'user_view'),
    (r'^attachment/(\d+)/$', 'attachment_view'),
)

class SearchForm(forms.Form):
    issue_types = forms.ChoiceField(choices=[
        (0, "All issues"),
        (1, "Open issues"),
        ], initial=1, required=False)
    search_text = forms.CharField(required=False)
    status = forms.CharField(required=False)
    priority = forms.CharField(required=False)
    product = forms.IntegerField(required=False)
    keyword = forms.IntegerField(required=False)

def index_view(request):
    form = SearchForm()
    bugs = Bugs.objects
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search_text"]
            status = form.cleaned_data["status"]
            issue_types = form.cleaned_data["issue_types"]
            product = form.cleaned_data["product"]
            priority = form.cleaned_data["priority"]
            keyword = form.cleaned_data["keyword"]

            bugs = bugs.filter(short_desc__icontains=search)
            if status != "":
                bugs = bugs.filter(bug_status__exact=status)
            if priority != "":
                bugs = bugs.filter(priority__exact=priority)
            if product:
                bugs = bugs.filter(product__exact=product)
            if keyword:
                bugs = bugs.filter(kws__id__exact=keyword)
            if issue_types == 1:
                bugs = bugs.exclude(bug_status__in=["CLOSED", "RESOLVED"])
    bugs = bugs.order_by("bug_id").reverse()
    return render_to_response("index.html", {
        "bugs": bugs,
        "form": form,
        "MEDIA_URL": settings.MEDIA_URL,
        })

def bug_view(request, bug_id):
    form = SearchForm()
    bug = Bugs.objects.get(bug_id=bug_id)
    prev_bug = int(bug_id)-1
    if len(Bugs.objects.filter(bug_id=prev_bug)) == 0:
        prev_bug = ""
    next_bug = int(bug_id)+1
    if len(Bugs.objects.filter(bug_id=next_bug)) == 0:
        next_bug = ""
    comments = bug.longdescs_set.all()
    comments_first = comments[0]
    comments_other = comments[1:]
    attachments = bug.attachments_set.all()
    return render_to_response("bug.html", {
        "bug": bug,
        "comments_first": comments_first,
        "comments_other": comments_other,
        "form": form,
        "prev_bug": prev_bug,
        "next_bug": next_bug,
        "attachments": attachments,
        "keywords": bug.kws.all(),
        "MEDIA_URL": settings.MEDIA_URL,
        })

def user_view(request, login_name):
    form = SearchForm()
    user = Profiles.objects.get(login_name__exact=login_name)
    return render_to_response("user.html", {
        "user": user,
        "form": form,
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
