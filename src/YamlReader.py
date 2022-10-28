from yaml import Loader, load
from pathlib import Path

class YamlReader:
    def __init__(self, path: Path):
        self.yaml = load(open(path, 'r'), Loader=Loader)

class ProgramsFile(YamlReader):
    def __init__(self, program: Path):
        super().__init__(program)
    
    def get(self):
        return self.yaml['programs']

class ConfigFile(YamlReader):
    def __init__(self):
        super().__init__(Path().cwd().joinpath(Path('config.yaml')))

    def get(self):
        return self.yaml['config']
