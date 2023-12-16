from django.shortcuts import render, redirect
from markdown2 import markdown
from django.utils.safestring import mark_safe
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    if title_name := util.get_entry(name):
        return render(request, "encyclopedia/titles.html", {
            "title": util.get_title(name),
            "body": mark_safe(markdown(title_name)),
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "body": mark_safe("<h1>Not Found</h1>"),
        })
    
def search(request):
    ls = util.list_entries()
    search = request.GET.get("q")
    if util.get_entry(search):
        return title(request, search)
    else:
        search_titles = []
        for li in ls:
            if search.lower() in li.lower():
                search_titles.append(li)
        return render(request, "encyclopedia/search.html", {
            "search_titles": search_titles
        })
    
def rand(request):
    rand_name = random.choice(util.list_entries())
    return title(request, rand_name)

def new_page(request):
    if request.method == "POST":
        header = request.POST.get("header")
        if util.get_entry(header):
            return render(request, "encyclopedia/error.html", {
                "body": mark_safe(f"<h1>The page named {header} already exists</h1>")
            }) 
        main_text = request.POST.get("markdown")
        util.save_entry(header, main_text)
        return redirect(f"../{header}")
        
    else:
        return render(request, "encyclopedia/new-page.html")
    
def edit(request, name):
    if request.method == "POST":
        util.save_entry(name, request.POST.get("edit"))
        return redirect(f"../{name}")
    else:
        return render(request, "encyclopedia/edit.html", {
            "body": util.get_entry(name),
            "title": name
        })

