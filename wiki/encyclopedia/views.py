from django.shortcuts import render
from . import util
from django.shortcuts import redirect
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    '''
    Return the entry text if util.get_entry finds a corresponding entry;
    return the 404 page if None is returned.
    '''
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })

def search(request):
    searchText = request.GET.get('q')
    if util.get_entry(searchText):
        return entry(request, searchText)
    else:
        matches = []
        for item in util.list_entries():
            if searchText in item:
                matches.append(item)
        return render(request, "encyclopedia/search_results.html", {
            "searchText": searchText,
            "matches": matches
        })
