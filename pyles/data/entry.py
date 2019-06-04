import json
from os import path, mkdir, listdir, remove
from operator import attrgetter
from shutil import rmtree
from win32com.client import Dispatch
from kivy.logger import Logger

from linktypes import manager
from data.paths import MAINDIR, LINKDIR
from data.manifest import get_manifest
from data.icon import from_save
from widgets.status_bar import status
from linktypes.settings import LinktypeException
from widgets.popup import question_dialog

class EntryException(ValueError):
    pass

def remove_entry(name):
    # Remove directory
    dir_path = path.join(MAINDIR, name)
    try:
        rmtree(dir_path)
    except OSError:
        text = 'Cannot delete data directory of entry {}'.format(name)
        Logger.exception('entry: {}'.format(text))
        raise EntryException(text)
    # Remove link
    link_path = path.join(LINKDIR, '{}.lnk'.format(name))
    try:
        remove(link_path)
    except OSError:
        text = 'Cannot delete link of entry {}'.format(name)
        Logger.exception('entry: {}'.format(text))
        raise EntryException(text)

class EntryList():
    _list = None
    
    def __init__(self):
        self.callbacks = []
        self.entries = []
        self.load_entries()
        
    def load_entries(self):
        # Iterate all directories in MAINDIR
        entry_names = [dir for dir in listdir(MAINDIR) if path.isdir(path.join(MAINDIR,dir))]
        errors = []
        for name in entry_names:
            try:
                entry = Entry(name)
                self.entries.append(entry)
            except EntryException as e:
                errors.append((name,e))

        # Show broken entries
        if errors:
            for error in errors:
                text = 'Could not load {}.\n{}\nDelete entry?'.format(error[0], error[1])
                question_dialog(text=text, on_yes=lambda: remove_entry(error[0]), on_no=None)

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

    def __len__(self):
        return len(self.entries)

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
            
    def initialize_new(self, name, icon, linktypeconfig):
        # Check if name is not empty
        if len(name) == 0:
            raise EntryException('Name cannot be empty.')
        self.name = name
        
        # Set members
        self._icon = icon
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
        
    def save(self, icon, linktypeconfig):
        # Set members
        self._icon = icon
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
        remove_entry(self.name)
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
        linktypeconfig_str = json.dumps(manager.serialize(self.linktypeconfig))
        with open(self.linktypeconfig_path, 'w') as linktypeconfig_file:
            linktypeconfig_file.write(linktypeconfig_str)
        manager.apply(self.linktypeconfig)
            
    def load_linktype(self):
        try:
            with open(self.linktypeconfig_path, 'r') as linktypeconfig_file:
                linktypeconfig_str = linktypeconfig_file.readline()
        except FileNotFoundError:
            raise EntryException('Missing linktypeconfig file for entry {}.'
                .format(self.name))
        try:
            self.linktypeconfig = manager.deserialize(
                json.loads(linktypeconfig_str))
        except LinktypeException as e:
            raise EntryException('Cannot load linktypeconfig for entry {}: {}'
                .format(self.name, e))
        
            
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
        return self.linktypeconfig['linktype']
        
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