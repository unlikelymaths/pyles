import json
from os import path

from data.paths import MAINDIR

SETTINGS_PATH = path.join(MAINDIR, 'settings.json')

class GlobalSettings():
    
    def __init__(self):
        self.load_settings()

    def load_settings(self):
        if path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, 'r') as settings_file:
                self.data = json.load(settings_file)
        else:
            self.data = {
                'paths': {},
                'entries': [],
                }
    
    def save_settings(self):
        with open(SETTINGS_PATH, 'w') as settings_file:
            json.dump(self.data, settings_file)
       
global_settings = GlobalSettings()