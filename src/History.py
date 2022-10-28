import os
import shutil
from pathlib import Path
from deepdiff import DeepDiff
from YamlReader import ConfigFile, YamlReader


class History:
    def __init__(self):
        self.old = Path().cwd().joinpath(ConfigFile().get()['history']['location']).joinpath(Path('Oldinstall.yaml'))
        self.actual = Path().cwd().joinpath(ConfigFile().get()['install']['location'])
    
    def exist(self):
        return self.old.exists()
    
    def diff(self):
        localDiff = {}
        dif = DeepDiff(YamlReader(self.old).yaml, YamlReader(self.actual).yaml, ignore_order=True)
        programRemoved = dif.get('iterable_item_removed')
        programAdd = dif.get('iterable_item_added')
        if programRemoved is not None:
            localDiff['remove'] = list(programRemoved.values())
        if programAdd is not None:
            localDiff['add'] = list(programAdd.values())
        return localDiff
    
    def update(self):
        os.makedirs(os.path.dirname(self.old), exist_ok=True)
        shutil.copyfile(self.actual, self.old)