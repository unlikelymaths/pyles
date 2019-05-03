from os import path, getenv, mkdir, system

MAINDIR = path.join(getenv('APPDATA'), 'Pyles')
LINKDIR = path.join(getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\10Pyles')

if not path.isdir(MAINDIR):
    mkdir(MAINDIR)
if not path.isdir(LINKDIR):
    mkdir(LINKDIR)