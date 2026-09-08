import logging, os
from datetime import datetime, timezone, timedelta

def TimeElapsedStr(dt: timedelta | None = None) -> str:
    if dt is None:
        return "h"
    sdt = str(dt).split(':')
    return f"{sdt[0]}h{sdt[1]}"

class LogManager:
    #logDir = None
    #logDay = None
    
    dt = datetime.now(timezone.utc) - timedelta(hours=4) # change log in the morning at 4am UTC
    logDay = dt.strftime('%d')
    logDir = f"./logs/{dt.strftime('%Y%m')}"

    if not os.path.exists(logDir):
        os.makedirs(logDir)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s |%(levelname)s| %(message)s',
        filename= os.path.join(logDir, "debug.log"),
        filemode='a',
        encoding='utf-8'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    
    @staticmethod
    def getLogFileName(shortTag: str | None = None) -> str:
#        if not LogManager.logDir:
#            LogManager.__init__()
        
        logDir = os.path.join(LogManager.logDir or "", f"{LogManager.logDay}{ " " + shortTag if shortTag else ''}.log")
        return logDir
    
    @staticmethod
    def GetServerLogger(Name: str) -> logging.Logger | None:
        srvlogger = logging.getLogger(Name)
        if not srvlogger.handlers:
            handler = logging.FileHandler(LogManager.getLogFileName(Name), mode='a', encoding='utf-8')
            handler.setFormatter(logging.Formatter('%(asctime)s |%(levelname)s| %(message)s'))
            srvlogger.addHandler(handler)
            srvlogger.setLevel(logging.INFO)
            srvlogger.propagate=False
        return srvlogger

    @staticmethod
    def getFavoriteLogger(playerName: str) -> logging.Logger:
        favlogger = logging.getLogger("F-"+playerName)
        if not favlogger.handlers:
            logFileName = os.path.join(LogManager.logDir or "", f"{playerName}.log")
            handler = logging.FileHandler(logFileName, mode='a', encoding='utf-8')
            handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
            favlogger.addHandler(handler)
            favlogger.setLevel(logging.INFO)
            favlogger.propagate=False
        return favlogger

gLogManager = LogManager()