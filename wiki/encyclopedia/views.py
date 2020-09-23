from django.shortcuts import render
from . import util


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