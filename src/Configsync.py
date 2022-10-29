#!/usr/bin/python3
import yaml
import shutil
from yaml import Loader
from pathlib import Path

class Directory:
    def __init__(self, path : Path, isLocal = False, isHome = False):
        self.path = path
        if isLocal:
            self.path = Path.cwd().joinpath(path)
        if isHome:
            self.path = Path.home().joinpath(path)
        self.isLocal = isLocal
        self.isHome = isHome
    
    def link(self, toDirectory: 'Directory'):
        toDirectory.remove_link()
        toDirectory.remove_folder()
        toDirectory.path.symlink_to(self.path, target_is_directory= True)
    
    def remove_link(self):
        if self.path.exists() and self.path.is_symlink():
            self.path.unlink()

    def remove_folder(self):
        if self.path.exists() and self.path.is_dir(): 
            shutil.rmtree(self.path)

class File:
    def __init__(self, path : Path, isLocal = False, isHome = False):
        self.path = path
        if isLocal:
            self.path = Path.cwd().joinpath(path)
        if isHome:
            self.path = Path.home().joinpath(path)
        self.isLocal = isLocal
        self.isHome = isHome
    
    def link(self, toDirectory: 'File'):
        toDirectory.remove_link()
        toDirectory.remove_folder()
        toDirectory.path.symlink_to(self.path)
    
    def remove_link(self):
        if self.path.exists() and self.path.is_symlink():
            self.path.unlink()

    def remove_folder(self):
        if self.path.exists() and self.path.is_file(): 
            self.unlink()

class Configuration:
    def __init__(self, path : Path):
        self.path = path
        self.path = path
        self.conf = yaml.load(open(self.path, 'r'), Loader=Loader)
    
    def programs(self):
        programs = []
        for program in self.conf['programs']:
            locations = []
            for location in program['locations']:
                local = {}
                local['type'] = location['type']
                isLocal = location['origin'].get('isLocal')
                isHome = location['to'].get('isHome')
                if location['type'] == 'directory':
                    local['origin'] = Directory(Path(location['origin']['location']),isLocal=isLocal)
                    local['to'] = Directory(Path(location['to']['location']),isHome=isHome)
                elif location['type'] == 'file':
                    local['origin'] = File(Path(location['origin']['location']),isLocal=isLocal)
                    local['to'] = File(Path(location['to']['location']),isHome=isHome)                    
                locations.append(local)
            programs.append(Program(program['name'], locations))
        return programs

class Program:
    def __init__(self, name, locations):
        self.name = name
        self.locations = locations

def execute(path):
    programs = Configuration(path).programs()
    for program in programs:
        print("Executing.... " + program.name)
        for location in program.locations:
            location['origin'].link(location['to'])
