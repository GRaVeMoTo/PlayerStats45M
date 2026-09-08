# Author: GRaVE
#
from datetime import date, datetime, timezone, timedelta
from CfxServer import CfxServer, CfxPlyer
from FavoritePlayers import FavoritePlayers, gFavoritePlayers
from LogManager import LogManager, gLogManager, TimeElapsedStr
import logging, os

class PlayerData:
    def __init__(self, name: str, id: int, ping: int ):
        self.id:int = id
        self.name = name
        self.lastping:int = ping
        self.loginTimeUtc:datetime|None = None
        self.logoffTimeUtc:datetime|None = None

    def __str__(self):
        name = self.name if ',' not in self.name or ' ' not in self.name else f"'{self.name}'"
        if self.loginTimeUtc and self.logoffTimeUtc:
            dt = TimeElapsedStr(self.logoffTimeUtc - self.loginTimeUtc) 
            return f"{name}#{str(self.id)}~{dt}"
        return f"{name}#{str(self.id)}"
    def __repr__(self):
        return self.__str__()

class ServerLogger:
    def __init__(self, Name: str, ServerId:str, ServerUrl: str) -> None:
        self.Name = Name
        self.ServerId = ServerId
        self.ServerUrl = ServerUrl
        self.Players : dict[int, PlayerData] = {}
        self.cachedIds : set[int] = set()
        self.lastId:int = 0 #last player id what we have seen
        self.oldestId:int = 0 #oldest player id what we have seen last update
        self.nextFullLogTime:datetime|None = None # teljes lista csak init es orankent, addig csak valtozasok loggolasa, hogy ne legyen tul sok üres log

        try:
            self.logger = LogManager.GetServerLogger(Name)
            self.server = CfxServer(ServerUrl, True)
        except Exception as e:
            logging.error(f"Unable to create server for {Name}: {e}")

    def UpdatePlayersFromServer(self) -> None:
        players = self.server.FetchPlayerList() if self.server is not None else None
        if players is None:
            logging.error(f"{self.Name} nem sikerült lekérdezni a játékosokat.")
            return

        oldestId:int = players[0].id if len(players) > 0 else self.lastId
        if oldestId < self.oldestId: # server restarted or empty, reset player list
            self.logger.info(f" --server restarted or empty--")
            logging.info(f"{self.Name} oldestId {oldestId} < {self.oldestId}, latest {self.lastId}, restart detected, resetting players info.")
            self.Shutdown() # logoff all players
            self.cachedIds.clear()
            self.Players.clear()
            self.lastId = 0

        lastId = players[-1].id if len(players) > 0 else self.lastId # players are litarly sorted by id, but we can assume that the last one is the highest id
        if self.lastId == lastId and len(players) == len(self.cachedIds):
            self.logger.debug(f"{self.Name} {len(players)} no changes.")
            return # no change

        plJoin:list[str] = list[str]() 
        plLeft:list[str] = list[str]() 
        currentIds:set[int] = {player.id for player in players}

        exitPlayers = self.cachedIds - currentIds
        for playerId in exitPlayers:
            if playerId in self.Players:
                pd = self.Players[playerId]
                pd.logoffTimeUtc = datetime.now(timezone.utc)
                plLeft.append(str(pd))
                
                gFavoritePlayers.UpdateOnlineStatus(self.Name, pd.name, playerId, False)
            else:
                logging.warning(f"{self.Name} playerId {playerId} not found in Players list, but was in cachedIds, #TODO")

        for player in players:
            if player.id not in self.cachedIds:
                plJoin.append(str(player))
                gFavoritePlayers.UpdateOnlineStatus(self.Name, player.name, player.id, True)

            if player.id >= self.lastId and player.id not in self.Players:
                pd = PlayerData(player.name, player.id, player.ping)
                pd.loginTimeUtc = datetime.now(timezone.utc)
                self.Players[player.id] = pd

        if (len(plLeft) > 0):
            self.logger.info(f"{len(players):03}::- " + ', '.join(plLeft))
        if (len(plJoin) > 0):
            self.logger.info(f"{len(players):03}::+ " + ', '.join(plJoin))

        self.lastId = lastId
        self.oldestId = oldestId
        self.cachedIds = currentIds
                    
    def Shutdown(self) -> None:
        plLefts:list[str] = list[str]() 
        for playerId, pd in self.Players.items():
            if pd.logoffTimeUtc is None:
                pd.logoffTimeUtc = datetime.now(timezone.utc)
                plLefts.append(str(pd))
                gFavoritePlayers.UpdateOnlineStatus(self.Name, pd.name, playerId, False)

        self.logger.info(f"{len(plLefts):03}::- " + ', '.join(plLefts))
