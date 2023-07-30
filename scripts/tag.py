class Tag:
    bg_colors = ['light_red', 'light_orange' ,'light_yellow', 'light_green', 'light_blue', 'light_purple']

    def __init__(self, tag_name, bg_color=None, tid=None):
        self.id = tid
        self.tag_name = tag_name
        self.bg_color = bg_color

    def update_tags_list(tags_list, tid, new_tag):
        for i in range(len(tags_list)):
            if int(tags_list[i].id) == int(tid):
                tags_list[i] = new_tag
        return tags_list

    def remove_tag_from_list(tags_list, tid):
        for t in tags_list:
            if t.id == tid:
                tags_list.remove(t)
        return tags_list