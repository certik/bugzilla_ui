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

from models import (Bugs, Attachments, Profiles, Longdescs, Products,
        Components, OpSys, RepPlatform, AttachData)
from forms import SearchForm, CommentForm, NewIssueForm

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
    (r'^bug/(\d+)/delete/(\d+)/$', 'bug_delete_comment'),
    (r'^u/(\S+)/$', 'user_view'),
    (r'^new/$', 'new_view'),
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

            bugs = bugs.filter(short_desc__icontains=search) | \
                    bugs.filter(longdescs__thetext__icontains=search)
            bugs = bugs.distinct()
            if status != "":
                bugs = bugs.filter(bug_status__exact=status)
            if priority != "":
                bugs = bugs.filter(priority__exact=priority)
            if product:
                bugs = bugs.filter(product__name__exact=product)
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
    if request.method == "POST" and request.user.is_authenticated():
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            text = comment_form.cleaned_data["comment_text"]
            attachment = request.FILES.get("attachment", None)
            if text != "" or attachment is not None:
                who = Profiles.objects.get(login_name=request.user.username)
                l = Longdescs(bug=bug, who=who)
                if attachment:
                    #text += "Got attachment: %s\n" % attachment
                    a = Attachments(bug=bug, submitter=who)
                    a.filename = attachment.name
                    a.creation_ts = datetime.datetime.today()
                    a.modification_time = datetime.datetime.today()
                    a.isobsolete = 0
                    a.isprivate = 0
                    a.isurl = 0
                    a.save()
                    d = AttachData(id=a)
                    d.thedata = attachment.read()
                    d.save()
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
    if len(comments) > 0:
        comments_first = comments[0]
    else:
        comments_first = None
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

@login_required
def new_view(request):
    if request.method == "GET":
        form  = NewIssueForm()
    else:
        assert request.method == "POST"
        form = NewIssueForm(data=request.POST)
        if form.is_valid():
            product = form.cleaned_data["product"]
            summary = form.cleaned_data["summary"]
            description = form.cleaned_data["description"]
            who = Profiles.objects.get(login_name=request.user.username)
            b = Bugs()
            b.short_desc = summary
            b.alias = None
            b.product = product
            # get the first row in the Versions table by default:
            b.version = product.versions_set.all()[0].value
            # get the first row in the Milestones table by default:
            b.target_milestone = product.milestones_set.all()[0].value
            try:
                b.component = Components.objects.filter(product=b.product).get(name="core")
            except Components.DoesNotExist:
                b.component = Components.objects.filter(product=b.product).all()[0]
            b.op_sys = OpSys.objects.get(value="All").value
            b.rep_platform = RepPlatform.objects.get(value="All").value
            b.priority = "Medium"
            b.bug_severity = "Minor"
            b.bug_status = "NEW"
            b.everconfirmed = 1 # NEW is a confirmed status
            b.assigned_to = who
            b.delta_ts = datetime.datetime.today()
            b.creation_ts = datetime.datetime.today()
            b.reporter = who
            b.votes = 0
            b.reporter_accessible = 1
            b.cclist_accessible = 1
            b.estimated_time = 0
            b.remaining_time = 0
            b.keywords = "s"
            b.save()
            l = Longdescs(bug=b, who=who)
            l.thetext = description
            l.bug_when = datetime.datetime.today()
            l.work_time = 0
            l.isprivate = 0
            l.already_wrapped = 0
            l.type = 0
            l.save()
            redirect_to = "/bugs-ui/bug/%s/" % b.bug_id
            return HttpResponseRedirect(redirect_to)
    return render_to_response("new.html", {
        "new_issue_form": form,
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
