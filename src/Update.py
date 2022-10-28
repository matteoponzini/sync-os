from traceback import print_tb
import ansible_runner
from pathlib import Path
from Configsync import execute
from Download import Donwnloader
from YamlReader import ConfigFile

class Interface:

    def __init__(self, name : str):
        self.name = name
        self.__programLocation = ConfigFile().get()['programs']['location'] 
    
    def path(self):
        return Path.cwd().joinpath(self.__programLocation).joinpath(Path(self.name))
    
    def exist(self):
        return self.path().exists() and self.path().is_dir()

class Program(Interface):

    def __init__(self, name : str):
        super().__init__(name)

    def install(self):
        installPath = super().path().joinpath(Path('install.yml'))
        if super().exist():
            self.execute(installPath)
        else: 
            outputDir = './programs/'
            test = self.remote()
            Donwnloader().download(url=test, name=self.name, output_dir=outputDir)
            self.execute(installPath)
        return None
    
    def execute(self, installPath):
        vaultPassword = ConfigFile().get()['ansible']['vault']['password_file']
        vault = ConfigFile().get()['ansible']['vault']['file']
        vaultPassword = Path().cwd().joinpath(Path(vaultPassword))
        vault = Path().cwd().joinpath(Path(vault))

        ansible_runner.run(playbook=str(installPath), extravars={'@':'./vault.yml'}, cmdline="--vault-password-file "+str(vaultPassword)+" -e @"+str(vault))

    def remove(self):
        pass
    
    def remote(self):
        url = ConfigFile().get()['repository']['app']+self.name
        print(url)
        return Donwnloader().remote(url)

class Config(Interface):
    def __init__(self, name : str):
        super().__init__(name)

    def install(self):
        if super().exist():
            installPath = super().path().joinpath('config.yaml')
            if installPath.exists():
                outputDir = './config/'
                Donwnloader().download(url=self.remote(), name=self.name, output_dir=outputDir)
                return execute(installPath)
        return None

    def remove(self):
        return None
    
    def remote(self):
        url = ConfigFile().get()['repository']['config']+self.name
        return Donwnloader().remote(url)