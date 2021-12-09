import json


class File:
    """handles files"""
    def __init__(self):
        """initialise the fle"""
        self.file_name = 'user_data.json'

    def _load_user_info(self):
        """open the file"""
        with open(self.file_name) as f:
            user_data = json.load(f)
            return user_data

    def _dump_user_info(self, user_data):
        """save the file"""
        with open(self.file_name, 'w') as f:
            json.dump(user_data, f)
    