from os.path import isdir, isfile, dirname, basename
from kivy.logger import Logger
from linktypes.type_settings import FilePathSetting, get_setting, LinktypeException

active = True
name = 'Default (exe)'

def config():
    return [
        FilePathSetting('path','Path'),
        ]
    
vbs_file_template = (
    'On Error Resume Next\n'
    'Set shell = CreateObject("Wscript.Shell")\n'
    'appPath = """{path_file}"""\n'
    'appPathDir = "{path_dir}"\n'
    'shell.CurrentDirectory = appPathDir\n'
    'shell.Run appPath')

vbs_dir_template = (
    'On Error Resume Next\n'
    'Set shell = CreateObject("Wscript.Shell")\n'
    'appPath = "explorer.exe ""{path}"""\n'
    'shell.Run appPath')
    
def get_vbs(config):
    path_setting = get_setting(config,'path')
    path = path_setting.value
    if isdir(path):
        return vbs_dir_template.format(path=path)
    elif isfile(path):
        path_file = '.\{}'.format(basename(path))
        path_dir = dirname(path)
        return vbs_file_template.format(path_file=path_file, path_dir=path_dir)
    else:
        raise LinktypeException('Path seems to be invalid.')
