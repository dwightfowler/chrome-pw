import os
import platform
import json
from configparser import ConfigParser


class FireFox():

    def __init__(self):
        self.installs, self.profiles = self.readProfile()

    def osName(self):
        sys = platform.system()
        if sys == 'Windows' or sys == 'Linux':
            return sys
        else:
            return None

    def dbPath(self, osName):
        print(f'{osName}')
        if osName == 'Windows':
            from os import environ
            userName = environ.get('USERNAME')
            return f'C:/Users/{userName}/AppData/Roaming/Mozilla/Firefox/'
        elif osName == 'Linux':
            return '~/.mozilla/firefox/'
        else:
            return None

    def readInis(self):
        sysName = self.osName()
        self.path = self.dbPath(sysName)
        parserInstalls = None
        parserProfiles = None
        if sysName == 'Windows' or sysName == 'Linux':
            installs = os.path.join(self.path, 'installs.ini')
            if not os.path.exists(installs):
                return (None, None)
            profiles = os.path.join(self.path, 'profiles.ini')
            if not os.path.exists(installs):
                return (None, None)
            try:
                parserInstalls = ConfigParser()
                parserInstalls.read(installs)
                parserProfiles = ConfigParser()
                parserProfiles.read(profiles)
            except Exception as e:
                print(e)

        return parserInstalls, parserProfiles


    def readProfile(self):
        result = (ins, pro) = self.readInis()
        return result

    def displayIni(self, ini:ConfigParser):
        for sectName, sect in ini.items():
            print(f'[{sectName}]')
            for key, value in sect.items():
                print(f'{key}={value}')
            print('')

    def _profilePath(self):
        self._profilePath = None
        for sectName, sect in self.installs.items():
            if sectName == 'DEFAULT':
                continue

            isDefault = False
            isLocked = False
            for key, value in sect.items():
                if not isDefault and key.lower() == 'default': 
                    isDefault = True
                    result = value
                if not isLocked and key.lower() == 'locked': 
                    isLocked = value == '1'
                if isDefault and isLocked:
                    self._profilePath = result
                    break

    def loginJson(self):
        self._profilePath()
        if not self._profilePath:
            return None

        path = os.path.join(self.path, self._profilePath)
        if os.path.exists(path):
            self.path = path
        else:
            return None
    
        self.loginsJson = os.path.join(self.path, 'logins.json')
        if os.path.exists(self.loginsJson):
            with open(self.loginsJson, 'r') as fp:
                result = json.load(fp)
        
        return result
