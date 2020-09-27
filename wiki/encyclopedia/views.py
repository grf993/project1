from . import util
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random

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
    textEntry = util.get_entry(title)
    if textEntry:
        md = markdown2.markdown(textEntry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": md
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })

def search(request):
    searchText = request.GET.get('q')
    # return page user searched for if exact match
    if util.get_entry(searchText):
        return entry(request, searchText)
    else:
        matches = []
        # add entry title to list if search text is contained in title
        for title in util.list_entries():
            if searchText in title:
                matches.append(title)
        # redirect to search results page with list of matches
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
    '''
    Get title from entry's "Edit" button form and redirect to editPage.html.
    Acts as the intermediary between the entry page and the edit page so that
    the edit page only has to handle one POST (to itself).
    '''
    if request.method == "POST":
        title = request.POST.get("title", "")
        textarea = util.get_entry(title)
        form = NewTextAreaForm(initial={'title': title, 'textarea': textarea})
        return render(request, "encyclopedia/editPage.html", {
            "form": form
        })

def randomPage(request):
    pageList = util.list_entries()
    randomNum = random.randint(0, len(pageList) - 1)
    title = pageList[randomNum]
    return entry(request, title)