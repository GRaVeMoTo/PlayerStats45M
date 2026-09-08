# -- coding: utf-8 --
# Author: GRaVE

from abc import abstractmethod

class DBInterface:
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def fetch_players(self) -> list:
        pass
    
    @abstractmethod
    def log_player_activity(self, player_id: str, activity: str):
        pass