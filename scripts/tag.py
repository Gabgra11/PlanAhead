class Tag:
    bg_colors = ["light_red", "light_orange" ,"light_yellow", "light_green", "light_blue", "light_purple"]

    def __init__(self, name, background_color, text_color):
        self.name = name
        self.background_color = background_color
        self.text_color = text_color

    def get_tag_by_name(tags_list, tag_name):
        for t in tags_list:
            if t.name == tag_name:
                return t
        return Tag("", "", "")

    def remove_empty_tags(tags_list):
        to_remove = []
        for t in tags_list:
            if t.name == "":
                to_remove.append(t)
        for t in to_remove:
            tags_list.remove(t)

    def add_blank_tag(tags_list):
        # Check for existing blank tag:
        for t in tags_list:
            if t.name == "" and t.background_color == "" and t.text_color == "":
                # Blank tag already exists
                return
        new_tag = Tag("", "", "")
        tags_list.insert(0, new_tag)
        
    def name_is_unique(tags_list, name):
        for t in tags_list:
            if t.name == name:
                return False
        return True