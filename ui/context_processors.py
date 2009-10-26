from forms import SearchForm

def search_form(request):
    search_form = SearchForm()
    return {"search_form": search_form}
