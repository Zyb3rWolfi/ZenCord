class Channel:

    def __init__(self, json_obj):
        self.channel_obj = json_obj
        self.id = json_obj["id"]