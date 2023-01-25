class Note:
    def __init__(self, title, body, tag=None, id=None):
        self.id = id
        self.title = title.strip()
        self.body = body
        self.tag = tag
        self.editing = False

    def update_notes_list(notes_list, nid, new_note):
        for i in range(len(notes_list)):
            if int(notes_list[i].id) == int(nid):
                notes_list[i] = new_note
        return notes_list