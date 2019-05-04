from os.path import dirname
from linktypes.type_settings import FilePathSetting

name = 'Default (exe)'

config = [
    FilePathSetting('path','Path'),
    ]
    
vbs_template = (
    'On Error Resume Next\n'
    'Set shell = CreateObject("Wscript.Shell")\n'
    'appPath = "{path}"\n'
    'appPathDir = "{path_dir}"\n'
    'shell.CurrentDirectory = appPathDir\n'
    'shell.Run(appPath)')

    
def get_vbs(config):
    path = config['path']
    path_dir = dirname(path)
    return vbs_template.format(path=path, path_dir=path_dir)