from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random
# Function to convert markdown content to HTML
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

# Index view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry view for each title
def entry(request, title):
    # Call the conversion function
    html_content = convert_md_to_html(title)
    
    # Check if content was found
    if html_content is None:
        # Render error page if content is not found
        return render(request, "encyclopedia/error.html",{
            "message":"this entry does not exit"
        })
    else:
        # Render the entry page with the title and HTML content
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
def search(request):
    if request.method =="POST":
        entry_search = request.POST.get('q')
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request,"encyclopedia/entry.html",
                          {
                              "title":entry_search,
                              "content":html_content
                          })
        else:
            allentries = util.list_entries()
            recommendation=[]
            for entry in allentries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request,"encyclopedia/search.html",{
                "recommendation": recommendation
                
            })
def new(request):
    if request.method =="GET":
        return render(request,"encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html",{
                "message": "Entry page already exits"
            })
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":html_content
            })

def edit(request):
    if request.method =="POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title":title,
           "content": content
        })
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content =convert_md_to_html(title)
        return render(request,"encyclopedia/entry.html",{
        "title":title,
        "content": content
    })


def rand(request):
    allEntries=  util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request,"encyclopedia/entry.html",{
        "title":rand_entry,
        "content":html_content

    })



    
