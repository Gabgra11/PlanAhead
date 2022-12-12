'''
TODO: Fix spacing on tag editor page between rows
TODO: Add delete button to notes on hover
TODO: Figure out how to directly input class string with Jinja
TODO: Enforce unique tag names
TODO: Implement search feature
TODO: Click on note to edit
TODO: Light/Dark mode toggle
TODO: DB integration
TODO: Calendar view
'''

from flask import Flask, render_template, request
from scripts import note, tag, user, search

app = Flask(__name__)

# For testing purposes:
curr_user = user.User()
t1 = tag.Tag("CS 374", "light_blue", "white")
t2 = tag.Tag("CS 411", "light_purple", "white")
t3 = tag.Tag("CS 412", "light_green", "white")
t4 = tag.Tag("CS 418", "light_yellow", "white")
curr_user.add_tags([t1, t2, t3, t4])

filters = set()

@app.route("/", methods=["GET", "POST"])
def home():
    global curr_user
    global filters

    notes_list = curr_user.notes

    if request.method == "POST":
        print(request.form["post_type"])
        if request.form["post_type"] == "filter_by_tag":
            filters.add(request.form["tag_name"])
            notes_list = search.filter_by_tags(curr_user.notes, filters)
        elif request.form["post_type"] == "remove_filter":
            filters.remove(request.form["tag_name"])
            notes_list = search.filter_by_tags(curr_user.notes, filters)
        elif request.form["post_type"] == "new_note":
            new_note = note.Note(request.form["title"], "", curr_user)
            curr_user.add_note(new_note)
        elif request.form["post_type"] == "search_notes":
            query = request.form["query"].strip() 
            if len(query) > 0:
                filters.add(query)
                notes_list = search.filter_by_text(curr_user.notes, query)
    else:
        filters.clear()

    tag.Tag.remove_empty_tags(curr_user.tags)
    note.Note.refresh_tags(curr_user.notes)

    return render_template("index.html", notes=notes_list, filter_tags=filters)

@app.route("/tags", methods=["GET", "POST"])
def tags():
    global curr_user

    if request.method == "POST":
        if request.form["post_type"] == "update":
            for t in curr_user.tags:
                if t.name == request.form["tag_name"]:
                    t.name = request.form["tag_name_input"]
                    t.background_color = request.form["bg_color_select"]
        elif request.form["post_type"] == "new_tag":
            curr_user.tags.insert(0, tag.Tag("", "", ""))
    else:
        tag.Tag.remove_empty_tags(curr_user.tags)
        note.Note.refresh_tags(curr_user.notes)
        
    return render_template("tags.html", tag_list = curr_user.tags, bg_colors = tag.Tag.bg_colors)

if __name__ == "__main__":
    app.run()