import logging, os
from datetime import datetime
from LogManager import LogManager, TimeElapsedStr

class FavoritePlayers:
    def __init__(self, configFile: str):
        self.configFile = configFile
        self.names = []

        if os.path.exists(configFile):
            with open(configFile, 'r', encoding='utf-8') as f:
                self.names = [line.strip() for line in f if line.strip()]

        self.OnlineStatus:list[bool] = [False] * len(self.names)
        self.StatusLogs:list[logging.Logger | None] = [None] * len(self.names)
        self.ConnectionTimes:list[datetime | None] = [None] * len(self.names)

    def IsFavorite(self, name: str) -> bool:
        return name in self.names
    
    def UpdateOnlineStatus(self, server: str, playerName: str, playerServerId:int, isOnline: bool) -> None:
        if playerName in self.names:
            index = self.names.index(playerName)
            if self.StatusLogs[index] is None:
                self.StatusLogs[index] = LogManager.getFavoriteLogger(playerName)

            duration = ""
            if isOnline : # and self.ConnectionTimes[index] is None
                self.ConnectionTimes[index] = datetime.now()
            elif not isOnline:
                if self.ConnectionTimes[index] is not None:
                    ct:datetime = self.ConnectionTimes[index]
                    duration = TimeElapsedStr(datetime.now() - ct)

            if  isOnline:
                self.StatusLogs[index].info(f"{server} ::+ #{playerServerId}")
            else:
                self.StatusLogs[index].info(f"{server} ::- #{playerServerId} {duration}")
            self.OnlineStatus[index] = isOnline

gFavoritePlayers = FavoritePlayers("./logfavs.config")