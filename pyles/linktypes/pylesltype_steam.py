import re
from os import path, mkdir, listdir, remove
from kivy.logger import Logger

from linktypes.type_settings import MultipleChoiceSetting, get_setting

active = True

def locate_steam_main():
    candidates = ['C:\\Program Files\\Steam',
        'C:\\Program Files (x86)\\Steam']
    for directory in candidates:
        if path.isdir(directory):
            exe_path = path.join(directory, 'Steam.exe')
            if path.isfile(exe_path):
                return directory
    return None

def add_appdir(appdirs, dir):
    appsdir = path.abspath(path.join(dir, 'steamapps'))
    if path.isdir(appsdir):
        commondir = path.join(appsdir, 'common')
        if path.isdir(commondir):
            appdirs.append(appsdir)
    return None
    
def read_libraryfolders(steam_main):
    libfolders_path = path.join(steam_main,'steamapps\\libraryfolders.vdf')
    if path.isfile(libfolders_path):
        with open(libfolders_path, 'r') as file:
            libfolders_str = file.read()
        candidates = libfolders_str.split('"')
        return [c for c in candidates if path.isdir(c)]
    return []
    
def read_appdirs(steam_main):
    appdirs = []
    add_appdir(appdirs, steam_main)
    libraryfolders = read_libraryfolders(steam_main)
    for dir in libraryfolders:
        add_appdir(appdirs, dir)
    return appdirs

def parse_manifest(dir, file):
    file_path = path.join(dir, file)
    name = None
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if '"name"' in line:
                m = re.match('.*"([^"]*)"\s*$',line)
                if m is not None and len(m.groups()) == 1:
                    name = m.groups()[0]
                break
    return name
    
def read_manifests(appdirs):
    games = []
    for appdir in appdirs:
        files = listdir(appdir)
        for file in files:
            m = re.match('appmanifest_([\d]*).acf',file)
            if m is None or len(m.groups()) != 1:
                continue
            id = m.groups()[0]
            name = parse_manifest(appdir, file)
            if id is not None and name is not None:
                games.append({'id': id, 'name': name})
    return games

if active:
    STEAM_MAIN = locate_steam_main()
    if STEAM_MAIN is not None:
        Logger.info('SteamLink: Found Steam at "{}".'.format(STEAM_MAIN))
    else:
        active = False

if active:
    APPDIRS = read_appdirs(STEAM_MAIN)
    if len(APPDIRS) > 0:
        Logger.info('SteamLink: Found {} steamapps directories.'.format(len(APPDIRS)))
    else:
        active = False

if active: 
    GAMES = read_manifests(APPDIRS)
    GAMENAMES = [game['name'] for game in GAMES]
    if len(GAMES) > 0:
        Logger.info('SteamLink: Found {} games.'.format(len(GAMES)))
    else:
        active = False

name = 'Steam Library'

def config():
    return [
        MultipleChoiceSetting('game','Game',GAMENAMES),
        ]

vbs_template = (
    'On Error Resume Next\n'
    'Set shell = CreateObject("Wscript.Shell")\n'
    'steamExe = """{steam_exe}"""\n'
    'steamPath = "{steam_path}"\n'
    'steamCommand = "steam://rungameid/{game_id}"\n'
    'shell.CurrentDirectory = steamPath\n'
    'shell.Run steamExe & steamCommand')

    
def get_vbs(config):
    game_setting = get_setting(config,'game')
    game_name = game_setting.value
    game = [game for game in GAMES if game['name'] == game_name][0]
    steam_exe = path.join(STEAM_MAIN, 'steam.exe')
    steam_path = STEAM_MAIN
    game_id = game['id']
    return vbs_template.format(steam_exe=steam_exe,
        steam_path=steam_path, game_id=game_id)