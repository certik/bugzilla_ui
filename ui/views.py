from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect
from django import forms

from models import Bugs

urlpatterns = patterns('bugzilla_ui.ui.views',
    (r'^$', 'index_view'),
    (r'^bug/(\d+)/$', 'bug_view'),
)

class SearchForm(forms.Form):
    issue_types = forms.ChoiceField(choices=[
        (0, "All issues"),
        (1, "Open issues"),
        ], initial=1)
    search_text = forms.CharField(required=False)

def index_view(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        assert form.is_valid()
        search = form.cleaned_data["search_text"]
        bugs = Bugs.objects.filter(short_desc__icontains=search). \
                order_by("bug_id").reverse()
    else:
        form = SearchForm()
        bugs = Bugs.objects.order_by("bug_id").reverse()
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
    return render_to_response("bug.html", {
        "bug": bug,
        "comments_first": comments_first,
        "comments_other": comments_other,
        "form": form,
        })

def redirect_index(request):
    return HttpResponseRedirect("ui/")
