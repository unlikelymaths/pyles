import json
from os import path, mkdir, listdir, remove
from operator import attrgetter
from shutil import rmtree
from win32com.client import Dispatch
from kivy.logger import Logger

from linktypes import linktype_manager
from data.paths import MAINDIR, LINKDIR
from data.manifest import get_manifest
from data.icon import from_save

class EntryException(ValueError):
    pass

class EntryList():
    _list = None
    
    def __init__(self):
        self.callbacks = []
        self.entries = []
        self.load_entries()
        
    def load_entries(self):
        # Iterate all directories in MAINDIR
        entry_names = [dir for dir in listdir(MAINDIR) if path.isdir(path.join(MAINDIR,dir))]
        for name in entry_names:
            try:
                entry = Entry(name)
                self.entries.append(entry)
            except Exception as e:
                Logger.warning('Entry: Cannot load config of entry "{}".'.format(name))
                raise e
                            
        # Remove all other links
        for link in listdir(LINKDIR):
            linkname = link.split('.')[0]
            if linkname not in entry_names:
                remove(path.join(LINKDIR,link))
                Logger.info('Entry: Removed orphaned link for "{}"'.format(linkname))

    def add_callback(self, callback):
        self.callbacks.append(callback)
      
    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback) 

    def notify(self):
        for callback in self.callbacks:
            callback(self)
        
    def add_entry(self, entry):
        if entry is not None and entry not in self.entries:
            self.entries.append(entry)
            self.sort_entries()
            self.notify()

    def remove_entry(self, entry):
        if entry in self.entries:
            self.entries.remove(entry)
            self.notify()
            
    def sort_entries(self):
        self.entries.sort(key=attrgetter('name'))

def get_entry_list():
    if EntryList._list == None:
        EntryList._list = EntryList()
    return EntryList._list
    
class Entry():
    def __init__(self, name, **kwargs):
        self._icon = None
        if len(kwargs) > 0:
            self.initialize_new(name, **kwargs)
        else:
            self.load(name)
            
    def initialize_new(self, name, icon, linktypename, linktypeconfig):
        # Check if name is not empty
        if len(name) == 0:
            raise EntryException('Name cannot be empty.')
        self.name = name
        
        # Set members
        self._icon = icon
        self.linktypename = linktypename
        self.linktypeconfig = linktypeconfig
            
        # Check if a link by that name already exists
        if path.isdir(self.path):
            raise EntryException('Name already exists.')
        
        # Create a directory
        try:
            mkdir(self.path)
            mkdir(self.full_icon_path)
        except OSError as e:
            if e.winerror == 123:
                raise EntryException('Cannot create folder. The name is not valid.')
            raise e
        
        # Write data
        self.write_vbs()
        self.write_manifest()
        self.write_linktype()
        self.write_icon()
        self.write_link()
        
        # Add to list
        get_entry_list().add_entry(self)
        
    def save(self, icon, linktypename, linktypeconfig):
        # Set members
        self._icon = icon
        self.linktypename = linktypename
        self.linktypeconfig = linktypeconfig
        
        # Write data
        self.write_vbs()
        self.write_manifest()
        self.write_linktype()
        self.write_icon()
        self.write_link()
            
    def load(self, name):
        self.name = name
        
        # Check if the corresponding link exists. Otherwise create
        if not path.isfile(self.link_path):
            self.write_link()
            Logger.info('Entry: Created missing link for "{}"'.format(self.name))
        
        # Try to load the linktype config
        self.load_linktype()
        
    def delete(self):
        # Remove directory
        rmtree(self.path)
        # Remove link
        remove(self.link_path)
        # Remove from list
        get_entry_list().remove_entry(self)
    
    def write_vbs(self):
        vbs_str = self.linktype.get_vbs(self.linktypeconfig)
        with open(self.vbs_path, 'w') as vbs_file:
            vbs_file.write(vbs_str)
            
    def write_manifest(self):
        manifest_str = get_manifest()
        with open(self.manifest_path, 'w') as manifest_file:
            manifest_file.write(manifest_str)
            
    def write_linktype(self):
        linktype = {'linktypename': self.linktypename,
            'linktypeconfig': linktype_manager.serialize(self.linktypeconfig)}
        linktypeconfig_str = json.dumps(linktype)
        with open(self.linktypeconfig_path, 'w') as linktypeconfig_file:
            linktypeconfig_file.write(linktypeconfig_str)
        linktype_manager.apply(self.linktypeconfig)
            
    def load_linktype(self):
        with open(self.linktypeconfig_path, 'r') as linktypeconfig_file:
            linktypeconfig_str = linktypeconfig_file.readline()
        linktype = json.loads(linktypeconfig_str)
        self.linktypename = linktype['linktypename']
        self.linktypeconfig = linktype_manager.deserialize(
            linktype['linktypeconfig'])
        
            
    def write_icon(self):
        if self._icon is not None:
            self._icon.save(self.full_icon_path)
            self._icon.save_as(self.icon_path)
            self._icon.save_as(self.ico_path)
        
    def write_link(self):
        link = Dispatch('WScript.Shell').CreateShortCut(self.link_path)
        link.Targetpath = self.vbs_path
        link.IconLocation = self.ico_path
        link.WorkingDirectory = self.path
        link.save()
        
    @property
    def icon(self):
        if self._icon is None:
            try:
                self._icon = from_save(self.full_icon_path)
            except:
                pass
        return self._icon
        
    @property
    def linktype(self):
        return linktype_manager.all[self.linktypename]
        
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
    def full_icon_path(self):
        return path.join(self.path, 'icon')
        
    @property
    def icon_path(self):
        return path.join(self.path, 'icon.jpg')
        
    @property
    def ico_path(self):
        return path.join(self.path, 'icon.ico')
        
    @property
    def link_path(self):
        return path.join(LINKDIR, '{}.lnk'.format(self.name))