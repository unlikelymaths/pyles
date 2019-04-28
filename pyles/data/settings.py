import json
from os import path, getenv, mkdir, system

MAINDIR = path.join(getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\10Pyles')
DATADIR = path.join(MAINDIR, 'data')
SETTINGS_PATH = path.join(DATADIR, 'settings.json')
    

def load_settings():
    if path.isfile(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as settings_file:
            settings = json.load(settings_file)
    else:
        settings = {
            'paths': {},
            'entries': [],
            }
    return settings
    
def save_settings(settings):
    return
    with open(SETTINGS_PATH, 'w') as settings_file:
        json.dump(settings, settings_file)
       
    
    
    


if not path.isdir(MAINDIR):
    mkdir(MAINDIR)
if not path.isdir(DATADIR):
    mkdir(DATADIR)