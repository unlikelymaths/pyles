import json
from os import path, mkdir, listdir, remove
from shutil import rmtree
from win32com.client import Dispatch
from kivy.logger import Logger

from linktypes import linktype_manager
from data.paths import MAINDIR, LINKDIR
from data.manifest import get_manifest

class EntryException(ValueError):
    pass

class EntryList():
    
    def __init__(self):
        self.entries = []
        self.load_entries()
        
    def load_entries(self):
        # Iterate all directories in MAINDIR
        entry_names = [dir for dir in listdir(MAINDIR) if path.isdir(path.join(MAINDIR,dir))]
        for name in entry_names:
            entry = Entry(name)
            self.entries.append(entry)
                            
        # Remove all other links
        for link in listdir(LINKDIR):
            linkname = link.split('.')[0]
            if linkname not in entry_names:
                remove(path.join(LINKDIR,link))
                Logger.info('Entry: Removed orphaned link for "{}"'.format(linkname))
            
    
class Entry():
    def __init__(self, name, **kwargs):
        if len(kwargs) > 0:
            self.initialize_new(name, **kwargs)
        else:
            self.load(name)
            
    def initialize_new(self, name, imagesection, linktypename, linktypeconfig):
        # Check if name is not empty
        if len(name) == 0:
            raise EntryException('Name cannot be empty.')
        self.name = name
            
            
        # Check if a link by that name already exists
        if path.isdir(self.path):
            raise EntryException('Name already exists.')
        
        # Create a directory
        try:
            mkdir(self.path)
        except OSError as e:
            if e.winerror == 123:
                raise EntryException('Cannot create folder. The name is not valid.')
            raise e
        
        # Set linktype and config
        self.linktype = linktype_manager.all[linktypename]
        self.linktypeconfig = linktypeconfig
        
        # Write data
        self.write_vbs()
        self.write_manifest()
        self.write_linktypeconfig()
        self.write_image(imagesection)
        self.write_link()
        
    def load(self, name):
        self.name = name
        
        # Check if the corresponding link exists. Otherwise create
        if not path.isfile(self.link_path):
            self.write_link()
            Logger.info('Entry: Created missing link for "{}"'.format(self.name))
    
    def delete(self):
        # Remove directory
        rmtree(self.path)
        # Remove link
        remove(self.link_path)
    
    def write_vbs(self):
        vbs_str = self.linktype.get_vbs(self.linktypeconfig)
        with open(self.vbs_path, 'w') as vbs_file:
            vbs_file.write(vbs_str)
            
    def write_manifest(self):
        manifest_str = get_manifest()
        with open(self.manifest_path, 'w') as manifest_file:
            manifest_file.write(manifest_str)
            
    def write_linktypeconfig(self):
        linktypeconfig_str = json.dumps(self.linktypeconfig)
        with open(self.linktypeconfig_path, 'w') as linktypeconfig_file:
            linktypeconfig_file.write(linktypeconfig_str)
            
    def write_image(self, imagesection):
        imagesection.save_as(self.icon_path)
        imagesection.save_as(self.ico_path)
        
    def write_link(self):
        link = Dispatch('WScript.Shell').CreateShortCut(self.link_path)
        link.Targetpath = self.vbs_path
        link.IconLocation = self.ico_path
        link.WorkingDirectory = self.path
        link.save()
        
    @property
    def path(self):
        return path.join(MAINDIR, self.name)
        
    @property
    def vbs_path(self):
        return path.join(self.path, '{}.vbs'.format(self.name))
        
    @property
    def manifest_path(self):
        return path.join(self.path, '{}.VisualElementsManifest.xml'.format(self.name))
                        
    @property
    def linktypeconfig_path(self):
        return path.join(self.path, 'linktypeconfig.json')
        
    @property
    def icon_path(self):
        return path.join(self.path, 'icon.jpg')
        
    @property
    def ico_path(self):
        return path.join(self.path, 'icon.ico')
        
    @property
    def link_path(self):
        return path.join(LINKDIR, '{}.lnk'.format(self.name))