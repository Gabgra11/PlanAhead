'''
TODO: Figure out how to directly input class string with Jinja
TODO: Implement create new note form
TODO: Add tag editor page
TODO: Implement search note/tage feature
TODO: Click on note to edit
TODO: Tag-based styling
TODO: Click on tag to sort by tag
TODO: Light/Dark mode toggle
TODO: DB integration
TODO: Calendar view
'''

from flask import Flask, render_template, request
from scripts import notes

app = Flask(__name__)

user_notes = [notes.Note("Test", "Hello World!", "light_red"), notes.Note("Foo", "Bar", "light_green")]

@app.route("/", methods=["GET", "POST"])
def home():
    global user_notes
    if request.method == "POST":
        user_notes.append(notes.Note(request.form["title"], "", "light_blue"))

    
    return render_template("index.html", notes=user_notes)

if __name__ == "__main__":
    app.run