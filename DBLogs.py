# Author: GRaVE
from DBInterface import DBInterface


class DBLogs(DBInterface):
    BaseDir:str = "Logs.db"
    LogRotation:str = "05:00" # 5 AM
    
    def __init__(self, DBDirectory: str):
        super().__init__()
        
    def connect(self):
        pass