'''
TODO: Figure out how to directly input class string with Jinja
TODO: Arrange cards properly
TODO: Implement create new note form
TODO: Add tag editor page
TODO: Implement search note/tage feature
TODO: Click on note to edit
TODO: Tag-based styling
TODO: Click on tag to sort by tag
TODO: Light/Dark mode toggle
TODO: DB integration
'''

from flask import Flask, render_template
from scripts import notes

app = Flask(__name__)

@app.route("/")
def home():
    user_notes = [notes.Note("Test", "Hello World!", "light_red"), notes.Note("Foo", "Bar", "light_green")]
    return render_template("index.html", notes=user_notes)

if __name__ == "__main__":
    app.run