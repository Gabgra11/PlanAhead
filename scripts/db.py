from scripts import note, tag, search
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Returns the ID of the new note
def add_new_note(n):
    conn = get_db_connection()
    command_beginning = 'INSERT INTO notes ('
    command_end = 'VALUES ('
    values = []

    # Build command strings and values list:
    if n.tag:
        command_beginning += 'tag, '
        command_end += '?, '
        values.append(str(n.tag.id))
    if n.title:
        command_beginning += 'title, '
        command_end += '?, '
        values.append(str(n.title))
    if n.body:
        command_beginning += 'body, '
        command_end += '?, '
        values.append(str(n.body))
    if n.date:
        command_beginning += 'date, '
        command_end += '?, '
        values.append(str(n.date))
    
    # Remove trailing commas and add closing parentheses:
    command_beginning = command_beginning[:-2] + ') '
    command_end = command_end[:-2] + ')'
    command = command_beginning + command_end

    # Execute command:
    new_note_id = conn.execute(command, tuple(values)).lastrowid
    conn.commit()
    return new_note_id

    # if n.tag:
    #     command = 'INSERT INTO notes (tag, title, body) VALUES (?, ?, ?)'
    #     new_note_id = conn.execute(command, (str(n.tag.id), str(n.title), str(n.body))).lastrowid
    # else:
    #     command = 'INSERT INTO notes (title, body) VALUES (?, ?)'
    #     new_note_id = conn.execute(command, (str(n.title), str(n.body))).lastrowid
    # conn.commit()
    # return new_note_id

# Returns the ID of the new tag, or None if tag name is a duplicate:
def add_new_tag(t):
    conn = get_db_connection()
    existing_tags = get_tags_list(conn)
    if search.validate_new_tag_name(existing_tags, t):
        command = 'INSERT INTO tags (tag_name, bg_color) VALUES (?, ?)'
        new_tag_id = conn.execute(command, (str(t.tag_name), str(t.bg_color))).lastrowid
        conn.commit()
        return new_tag_id
    else:
        # TODO: Handle invalid tag name case
        print("Tag name '%s' is invalid" %(t.tag_name))
        return None

def get_note_by_id(nid):
    conn = get_db_connection()
    command = 'SELECT * from notes where id = ?'
    return conn.execute(command, (str(nid),)).fetchone()

def get_tag_by_id(tid):
    conn = get_db_connection()
    command = 'SELECT * from tags WHERE id = ?'
    query = conn.execute(command, (str(tid),)).fetchone()
    if query:
        tid = query[0]
        tag_name = query[1]
        bg_color = query[2]

        return tag.Tag(tag_name, bg_color, tid)
    else:
        return None

# Replaces the note with the given note id with the contents of new_note
def update_note(nid, new_note):
    conn = get_db_connection()
    command = 'UPDATE notes SET '
    values = []

    # Build command strings and values list:
    if new_note.tag:
        command += 'tag = ?,'
        values.append(str(new_note.tag.id))
    if new_note.title:
        command += 'title = ?,'
        values.append(str(new_note.title))
    if new_note.body:
        command += 'body = ?,'
        values.append(str(new_note.body))
    if new_note.date:
        command += 'date = ?,'
        values.append(str(new_note.date))
    
    # Remove trailing comma and complete the command string:
    command = command[:-1]
    command += ' WHERE id = ?'
    values.append(str(nid))

    # Execute command:
    conn.execute(command, tuple(values))
    conn.commit()

# Replaces the tag with the given tag id with the contents of new_tag
def update_tag(tid, new_tag):
    conn = get_db_connection()
    if search.validate_new_tag_name(get_tags_list(conn), new_tag):
        command = 'UPDATE tags SET tag_name = ?, bg_color = ? WHERE id = ?'
        conn.execute(command, (str(new_tag.tag_name), str(new_tag.bg_color), str(tid)))
        conn.commit()
    else:
        # TODO: Handle invalid tag name
        print("Tag name '%s' is a duplicate" %(new_tag.tag_name))

def remove_note(nid):
    conn = get_db_connection()
    command = 'DELETE From notes WHERE id = ?'
    conn.execute(command, (str(nid),))
    conn.commit()

def remove_tag(tid):
    conn = get_db_connection()
    command = 'DELETE from tags WHERE id = ?'
    conn.execute(command, (str(tid),))
    conn.commit()

def get_notes_list():
    conn = get_db_connection()
    query = conn.execute('SELECT * FROM notes n LEFT JOIN tags t ON n.tag = t.id;').fetchall()
    notes_list = []
    for r in query:
        nid = r[0]
        tid = r[2]
        title = r[3]
        body = r[4]
        date = r[5]
        tag_name = r[7]
        bg_color = r[8]

        note_tag = tag.Tag(tag_name, bg_color, tid)
        notes_list.append(note.Note(title, body, note_tag, nid, date=date))
    return notes_list

def get_tags_list():
    conn = get_db_connection()
    query = conn.execute('SELECT * FROM tags;').fetchall()
    tags_list = []
    for r in query:
        tid = r[0]
        tag_name = r[1]
        bg_color = r[2]

        tags_list.append(tag.Tag(tag_name, bg_color, tid))
    return tags_list