import random
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse

from . import util
import markdown2
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(entry_content)
        })

def search(request):
    query = request.GET.get("q", "").strip()
    if query:
        exact_match = util.get_entry(query)
        if exact_match:
            return redirect(reverse("entry", args=[query]))
        else:
            results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "query": query
            })
    return redirect(reverse("index"))

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "existing": True,
                    "title": title
                })
            util.save_entry(title, content)
            return redirect(reverse("entry", args=[title]))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(reverse("entry", args=[title]))
    else:
        entry_content = util.get_entry(title)
        if entry_content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        form = EditPageForm(initial={"content": entry_content})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect(reverse("entry", args=[random_title]))