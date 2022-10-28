#!/usr/bin/python3
from pathlib import Path
from operator import methodcaller
from Update import Program, Config
from watchdog.events import FileSystemEventHandler
from YamlReader import ProgramsFile
from History import History

class MonitorFolder(FileSystemEventHandler):
    
    def __init__(self, type):
        self.type = type

    def on_modified(self, event):
        path = Path().cwd().joinpath(Path(event.src_path))
        if path.is_file():
            self.startSync(path)

    def startSync(self, path):
        Sync(self.type).startSync(path)

class Sync:
    def __init__(self, type):
        self.type = type
    
    def startSync(self, path):
        history = History()
        if not history.exist():
            for program in ProgramsFile(path).get():
                caller = methodcaller(self.type)
                caller(Program(program))
                caller(Config(program))
            history.update()
        else:
            diff = history.diff()
            if diff:
                if diff.get('add') is not None:
                    for program in diff['add']:
                        caller = methodcaller('install')
                        caller(Program(program))
                        caller(Config(program)) 
            history.update()