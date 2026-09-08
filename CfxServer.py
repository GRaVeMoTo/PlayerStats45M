# -- coding: utf-8 --
# Author: GRaVE
#

import logging
from os import stat
import httpx
from typing import ClassVar
#from curl_cffi import requests

class CfxPlyer:
    def __init__(self, name: str, id: int, ping: int ):
        self.id:int = id
        self.name = name
        self.ping = ping
        self.indentifiers = None # private or deprecated or remove by fivem: security reason
        #self.endpoint     # deprecated or remove by fivem: security reason

    def __str__(self):
        name = self.name if ',' not in self.name or ' ' not in self.name else f"'{self.name}'"
        return f"{name}#{str(self.id)}"
        #return f"{self.name} ({self.id}) {self.ping}ms"
    def __repr__(self):
        return self.__str__()

class TestPlayerList:
    players = [ CfxPlyer("Alnia" , 206, 28), CfxPlyer("Alf0nsine" , 214, 32), CfxPlyer("B0b" , 215, 45), CfxPlyer("Charlie" , 216, 28) ]

    @staticmethod
    def GetPlayers():
        pc = TestPlayerList.players
        TestPlayerList.players = TestPlayerList.players[1:]
        return pc

class CfxServer:
    API_BASE_URL = 'https://servers-frontend.fivem.net/api'

    SERVERS_ICON_URL = 'https://servers-live.fivem.net/servers/icon'
    DEFAULT_REFRESH_TIME = 60 # seconds

    # Class-level default headers. Annotated as ClassVar to indicate it's not
    # intended to be an instance mutable default. Instances will copy this
    # into self.headers in __init__ to avoid shared mutable state.
    DEFAULT_HEADERS: ClassVar[dict] = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Referer': 'https://servers.fivem.net/',
        'Origin': 'https://servers.fivem.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
    }

    def __init__(self, ServerIdOrUrl:str, directConnect = None):
        self.ServerIdOrUrl = ServerIdOrUrl
        # fivem server not working because of cloudflare bot protection, use directConnect to server
        self.directConnect = directConnect if directConnect is not None else ServerIdOrUrl.startswith("http")

        # copy class-level default headers to instance to avoid mutating shared dict
        self.headers = dict(self.DEFAULT_HEADERS)

        try:
            self.Client = httpx.Client(headers=self.headers, default_encoding="utf-8")
            logging.getLogger("httpx").setLevel(logging.WARNING)

        except Exception as e:
            print(f"Error: Unable to create HTTP client: {e}")


    def FetchPlayerList(self) -> list[CfxPlyer] | None:
        #if __debug__ : return TestPlayerList.GetPlayers()
        try:
            url = f"{self.ServerIdOrUrl}/players.json?token=1" if self.directConnect else f"{self.API_BASE_URL}/servers/single/{self.ServerIdOrUrl}" 
            resp = self.Client.get(url) if self.directConnect else None #requests.get(url, impersonate='chrome120', timeout=10)
            if resp:
                if resp.status_code == 200:
                    playerList = resp.json() #Players
                    if isinstance(playerList,list):
                        currentPlayers:list[CfxPlyer] = []
                        for player in playerList:
                            pd = CfxPlyer(player.get('name','unknown'), player.get('id', -1), player.get('ping',-1))
                            identifiers = player.get('identifiers', None)
                            if identifiers is not None and len(identifiers) > 0:
                                pd.indentifiers = identifiers
                                print(player['identifiers'])
                            currentPlayers.append(pd)

                        return sorted(currentPlayers, key=lambda p: p.id) if currentPlayers is not None and len(currentPlayers) > 0 else currentPlayers
                    else:
                        logging.error(f"Invalid response format from server. Expected a list but got {type(playerList)}, #TODO")
                else:
                    logging.error(f"Failed to fetch player list. Status code: {resp.status_code}, Response: {resp.text[0:120] if resp.text and len(resp.text) > 120 else ''}")
                
        except Exception as e:
            logging.error(f"{self.ServerIdOrUrl} Unable FetchPlayerList: exception: {e}")

        return None
