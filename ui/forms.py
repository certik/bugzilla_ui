from django import forms
from models import Products

class ProductChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name

class SearchForm(forms.Form):
    issue_types = forms.ChoiceField(choices=[
        (0, "All issues"),
        (1, "Open issues"),
        ], initial=1, required=False)
    search_text = forms.CharField(required=False)
    status = forms.CharField(required=False)
    priority = forms.CharField(required=False)
    product = forms.CharField(required=False)
    keyword = forms.IntegerField(required=False)

class CommentForm(forms.Form):
    comment_text = forms.CharField(required=False,
            widget=forms.Textarea(attrs={"cols": "80"}))

class NewIssueForm(forms.Form):
    product = ProductChoiceField(
            queryset=Products.objects.all().order_by("name"),
            empty_label=None,
            required=True)
    summary = forms.CharField(required=True)
    description = forms.CharField(required=True,
            widget=forms.Textarea(attrs={"cols": "80"}))
