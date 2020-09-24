from django.shortcuts import render
from . import util
from django.shortcuts import redirect
from django.urls import reverse
from django import forms

class NewTextAreaForm(forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(label="", widget=forms.Textarea())

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

def newPage(request):
    # execute this if user is submitting form
    if request.method == "POST":
        form = NewTextAreaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            # check if page already exists; print error if exists, save otherwise
            if util.get_entry(title):
                return render(request, "encyclopedia/newPage.html", {
                    "form": form,
                    "errorMsg": f"Page \"{title}\" already exists."
                })
            else:
                util.save_entry(title, textarea)
                return entry(request, title)
        else:
            # return back form with existing values if not valid
            return render(request, "encyclopedia/newPage.html", {
                "form": form,
                "errorMsg": "Invalid form. Please try again."
            })
    # execute this if user simply visiting page (not submitting form)
    return render(request, "encyclopedia/newPage.html", {
        "form": NewTextAreaForm()
    })

def editPage(request):
    '''
    Similar to newPage function but without same-title check and GET request handling
    '''
    if request.method == "POST":
        form = NewTextAreaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/editPage.html", {
                "form": form,
                "errorMsg": "Invalid form. Please try again."
            })

def getTitleFromEntry(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        textarea = util.get_entry(title)
        form = NewTextAreaForm(initial={'title': title, 'textarea': textarea})
        return render(request, "encyclopedia/editPage.html", {
            "form": form
        })