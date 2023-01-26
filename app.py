'''
TODO: Cache notes and tags, only update local version when changes are made.
TODO: Optional warning when deleting notes/tags
TODO: Don't hard code color options
TODO: Calendar view
'''

from flask import Flask, render_template, request
from scripts import note, tag, search, db, tagparser
import sqlite3

app = Flask(__name__)

notes_list = []
tags_list = []

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    global notes_list
    global tags_list

    filter_list = []
    conn = get_db_connection()
    notes_list = db.get_notes_list(conn)

    if request.method == "POST":
        match request.form["post_type"]:
            case "new_note":
                title = request.form["title"]
                t = tagparser.parse_title_for_tag(title, tags_list)
                n = note.Note(title, "", t)  # TODO: Add body
                n.id = db.add_new_note(conn, n)
                notes_list.append(n)
            case "filter_by_tag":
                new_filter_id = request.form['filter_tag']
                filter_list.append(db.get_tag_by_id(conn, new_filter_id))
                notes_list = search.filter_by_tags(notes_list, filter_list)
            case "edit_mode":
                note_id = request.form['note_id']
                for i in range(len(notes_list)):
                    if notes_list[i].id == int(note_id):
                        notes_list[i].editing = True
            case "edit_note":
                note_id = request.form['note_id']
                new_title = request.form['new_title']
                new_tag = db.get_tag_by_id(conn, request.form['new_tag'])
                new_body = request.form['new_body']
                new_note = note.Note(new_title, new_body, new_tag, note_id)
                db.update_note(conn, note_id, new_note)
                notes_list = note.Note.update_notes_list(notes_list, note_id, new_note)


    return render_template("index.html", notes=notes_list, filter_list=filter_list, tags_list=db.get_tags_list(conn))

@app.route("/tags", methods=["GET", "POST"])
def tags():
    global tags_list

    conn = get_db_connection()
    if request.method == 'POST':
        match request.form['post_type']:
            case "new_tag":
                tag_name = request.form['tag_name']
                if len(tag_name) > 0:   # Prevent blank tag names
                    t = tag.Tag(tag_name)
                    new_tag_id = db.add_new_tag(conn, t)
                    if new_tag_id:
                        t.id = new_tag_id
                        tags_list.append(t)
                    else:   # Tag name is not unique
                        #TODO: Notify the user
                        print("Tag name '%s' is not valid." %(t.tag_name))

            case "update_tag":  # TODO: Update the tags of all notes with old tag
                tag_id = request.form['tag_id']
                new_tag_name = request.form['new_tag_name']
                new_bg_color = request.form['new_bg_color']
                if len(new_tag_name) > 0:   # Prevent blank tag names
                    new_tag = tag.Tag(new_tag_name, new_bg_color, tag_id)
                    tags_list = tag.Tag.update_tags_list(tags_list, tag_id, new_tag)
                    db.update_tag(conn, tag_id, new_tag)
            case "delete_tag":
                tag_id = request.form['tag_id']
                tags_list = tag.Tag.remove_tag(tags_list, tag_id)
                db.remove_tag(conn, tag_id)

    return render_template("tags.html", bg_colors=tag.Tag.bg_colors, tags_list=db.get_tags_list(conn))

if __name__ == "__main__":
    app.run()