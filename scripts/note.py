from scripts import tag, user

class Note:
    def __init__(self, title, body, user):
        self.title = title
        self.title_index = 0
        self.body = body
        self.user = user
        self.tag = None # Is this needed?
        self.parse_title()

    def parse_title(self):
        for t in self.user.tags:
            tag_index = self.title.lower().find(t.name.lower())
            if tag_index == 0:
                self.tag = t
                self.title_index = tag_index + len(t.name)
                return
        self.title_index = 0
        self.tag = None
    