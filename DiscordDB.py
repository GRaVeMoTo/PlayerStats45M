class DiscordDB:
    def __init__(self):
        self.configFile = "discord.db"
        self.IdMap:dict[str, int] = {}

        with open(self.configFile, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    id, name = line.strip().split(' ', 1)
                    self.IdMap[name] = int(id)

