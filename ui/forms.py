from django import forms

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

class CommentForm(forms.Form):
    comment_text = forms.CharField(required=False,
            widget=forms.Textarea(attrs={"cols": "80"}))
