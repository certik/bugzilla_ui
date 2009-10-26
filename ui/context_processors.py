from forms import SearchForm

def search_form(request):
    search_form = SearchForm()
    return {"search_form": search_form}

def request_path(request):
    return {"request_path": request.path}
