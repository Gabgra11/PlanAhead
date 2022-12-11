from scripts import tag, user

class Note:
    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user
        self.tag = None # Is this needed?
        self.parse_title()

    def parse_title(self):
        for t in self.user.tags:
            print(t.name)
            if t.name in self.title:
                self.tag = t
                return
    