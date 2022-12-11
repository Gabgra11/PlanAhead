class User:
    def __init__(self):
        self.tags = []
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def add_tags(self, tags_list):
        for t in tags_list:
            self.tags.append(t)