import datetime

from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail
from django.template import RequestContext
from django.db.models import Q

from models import Bugs, Attachments, Profiles, Longdescs
from forms import SearchForm, CommentForm

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
    (r'^bug/(\d+)/delete/(\d+)/$', 'bug_delete_comment'),
    (r'^u/(\S+)/$', 'user_view'),
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
    (r'^attachment/(\d+)/$', 'attachment_view'),
)

def index_view(request):
    search_form = SearchForm()
    bugs = Bugs.objects
    if request.method == "GET":
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data["search_text"]
            status = search_form.cleaned_data["status"]
            issue_types = search_form.cleaned_data["issue_types"]
            product = search_form.cleaned_data["product"]
            priority = search_form.cleaned_data["priority"]
            keyword = search_form.cleaned_data["keyword"]

            bugs = bugs.filter(Q(short_desc__icontains=search) | \
                    Q(longdescs__thetext__icontains=search))
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
        "search_form": search_form,
        },
        context_instance=RequestContext(request))

@login_required
def bug_delete_comment(request, bug_id, comment_id):
    bug = Bugs.objects.get(bug_id=bug_id)
    comment = bug.longdescs_set.get(comment_id=comment_id)
    if request.user.username == comment.who.login_name:
        comment.delete()
        return HttpResponseRedirect("/bugs-ui/bug/%s/" % bug_id)
    else:
        raise Http404

def bug_view(request, bug_id):
    bug = Bugs.objects.get(bug_id=bug_id)
    if request.method == "GET" and request.user.is_authenticated():
        comment_form = CommentForm(request.GET)
        if comment_form.is_valid():
            text = comment_form.cleaned_data["comment_text"]
            if text != "":
                who = Profiles.objects.get(login_name=request.user.username)
                l = Longdescs(bug=bug, who=who)
                l.thetext = text
                l.bug_when = datetime.datetime.today()
                l.work_time = 0
                l.isprivate = 0
                l.already_wrapped = 0
                l.type = 0
                l.save()
                return HttpResponseRedirect("/bugs-ui/bug/%s/" % bug_id)
    comment_form = CommentForm()
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
        "comment_form": comment_form,
        "prev_bug": prev_bug,
        "next_bug": next_bug,
        "attachments": attachments,
        "keywords": bug.kws.all(),
        },
        context_instance=RequestContext(request))

def user_view(request, login_name):
    user = Profiles.objects.get(login_name__exact=login_name)
    return render_to_response("user.html", {
        "user_info": user,
        },
        context_instance=RequestContext(request))

def login_view(request):
    if request.method == "GET":
        login_form  = AuthenticationForm()
    else:
        assert request.method == "POST"
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            redirect_to = request.REQUEST.get("next", "/bugs-ui/")
            return HttpResponseRedirect(redirect_to)
    return render_to_response("login.html", {
        "login_form": login_form,
        "next": request.REQUEST.get("next", "/bugs-ui/")
        },
        context_instance=RequestContext(request))

def logout_view(request):
    return logout(request, next_page=request.REQUEST.get("next", "/bugs-ui/"))

def attachment_view(request, attach_id):
    attachment = Attachments.objects.get(attach_id=attach_id)
    data = attachment.attachdata_set.get().thedata
    response = HttpResponse(data)
    response["Content-Disposition"] = "attachment; filename=%s" % \
            attachment.filename
    return response

def redirect_index(request):
    return HttpResponseRedirect("/bugs-ui/")
