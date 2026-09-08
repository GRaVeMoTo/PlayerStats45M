# -- coding: utf-8 --
# Author: GRaVE
#
from datetime import datetime, timedelta, timezone
import logging
import os
from time import sleep
import time
from ServerLogger import ServerLogger

def checkForcreQuit():
    if os.path.exists("restart.force") and os.path.getsize("restart.force") >= 1:
        with open("restart.force", "w") as f:
            f.truncate(0)
            f.seek(0)
            f.write("")
        return True
    return False

def LoggersShutdown(servers: list[ServerLogger]) -> None:
    logging.info("Force quit detected, exiting...")
    for server in servers:
        server.Shutdown()

if __name__ == "__main__":

    servers = [ 
        #ServerLogger ("GLXY", "933gab", "https://play.galaxyrp.hu:30120") # Galaxy
        ServerLogger ("GLXY", "933gab", "https://play.galaxyrp.hu:443") # Galaxy
       # , ServerLogger( "WLKR", "d7xdbj", "https://play.walkure.hu:443") # Walkure
    ]

    try:
        while True:
            start = datetime.now(timezone.utc)
            for server in servers:
                server.UpdatePlayersFromServer()
            end = datetime.now(timezone.utc)
            elapsed = (start+timedelta(seconds=60)-end).total_seconds()
            
            if checkForcreQuit():
                LoggersShutdown(servers)
                exit(0)

            sleep(max(10, elapsed))
                            
    except (KeyboardInterrupt, EOFError):
        LoggersShutdown(servers)
        raise KeyboardInterrupt