from scripts import note, tag, search

# Returns the ID of the new note
def add_new_note(conn, n):
    if n.tag:
        command = 'INSERT INTO notes (tag, title, body) VALUES (?, ?, ?)'
        new_note_id = conn.execute(command, (str(n.tag.id), str(n.title), str(n.body))).lastrowid
    else:
        command = 'INSERT INTO notes (title, body) VALUES (?, ?)'
        new_note_id = conn.execute(command, (str(n.title), str(n.body))).lastrowid
    conn.commit()
    return new_note_id

# Returns the ID of the new tag, or None if tag name is a duplicate:
def add_new_tag(conn, t):
    existing_tags = get_tags_list(conn)
    if search.check_duplicate_tag_names(existing_tags, t):
        # TODO: Handle duplicate tag name
        print("Tag name '%s' is a duplicate" %(t.tag_name))
        return None
    else:
        command = 'INSERT INTO tags (tag_name, bg_color) VALUES (?, ?)'
        new_tag_id = conn.execute(command, (str(t.tag_name), str(t.bg_color))).lastrowid
        conn.commit()
        return new_tag_id

def get_note_by_id(conn, nid):
    command = 'SELECT * from notes where id = ?'
    return conn.execute(command, (str(nid),)).fetchone()

def get_tag_by_id(conn, tid):
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
def update_note(conn, nid, new_note):
    if new_note.tag:
        command = 'UPDATE notes SET tag = ?, title = ?, body = ? WHERE id = ?'
        conn.execute(command, (str(new_note.tag.id), str(new_note.title), str(new_note.body), str(nid)))
    else:
        command = 'UPDATE notes SET title = ?, body = ? WHERE id = ?'
        conn.execute(command, (str(new_note.title), str(new_note.body), str(nid)))
    conn.commit()

# Replaces the tag with the given tag id with the contents of new_tag
def update_tag(conn, tid, new_tag):
    if search.check_duplicate_tag_names(get_tags_list(conn), new_tag):
        # TODO: Handle duplicate tag name
        print("Tag name '%s' is a duplicate" %(new_tag.tag_name))
    else:
        command = 'UPDATE tags SET tag_name = ?, bg_color = ? WHERE id = ?'
        conn.execute(command, (str(new_tag.tag_name), str(new_tag.bg_color), str(tid)))
        conn.commit()

def remove_note(conn, nid):
    command = 'DELETE From notes WHERE id = ?'
    conn.execute(command, (str(nid),))
    conn.commit()

def remove_tag(conn, tid):
    command = 'DELETE from tags WHERE id = ?'
    conn.execute(command, (str(tid),))
    conn.commit()

def get_notes_list(conn):
    query = conn.execute('SELECT * FROM notes n LEFT JOIN tags t ON n.tag = t.id;').fetchall()
    notes_list = []
    for r in query:
        nid = r[0]
        tid = r[2]
        title = r[3]
        body = r[4]
        tag_name = r[6]
        bg_color = r[7]

        note_tag = tag.Tag(tag_name, bg_color, tid)
        notes_list.append(note.Note(title, body, note_tag, nid))
    return notes_list

def get_tags_list(conn):
    query = conn.execute('SELECT * FROM tags;').fetchall()
    tags_list = []
    for r in query:
        tid = r[0]
        tag_name = r[1]
        bg_color = r[2]

        tags_list.append(tag.Tag(tag_name, bg_color, tid))
    return tags_list