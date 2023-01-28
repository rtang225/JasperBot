import json
f = open('config.json')
config = json.load(f)

class BotConfig:
    @staticmethod
    def token() -> str:
        return config["bot"]["token"]

    @staticmethod
    def db() -> str:
        return config["bot"]["db"]
    
    @staticmethod
    def prefix() -> str:
        return config["bot"]["prefix"]
    
    @staticmethod
    def color() -> int:
        return int(config["bot"]["color"], 16)

    @staticmethod
    def footer() -> str:
        return config["bot"]["footer"]

    @staticmethod
    def lcss_id() -> int:
        return config["lcss"]["id"]

    @staticmethod
    def log_id() -> int:
        return config["log"]["id"]

    @staticmethod
    def lcss_logs() -> int:
        return config["lcss"]["channels"]["logs"]

    @staticmethod
    def lcss_punishments() -> int:
        return config["lcss"]["channels"]["punishment"]

    @staticmethod
    def lcss_botsetup() -> int:
        return config["lcss"]["channels"]["botsetup"]

    @staticmethod
    def lcss_membercount() -> int:
        return config["lcss"]["channels"]["membercount"]

    @staticmethod
    def lcss_identify() -> int:
        return config["lcss"]["channels"]["identify"]

    @staticmethod
    def lcss_general() -> int:
        return config["lcss"]["channels"]["general"]

    @staticmethod
    def lcss_welcome() -> int:
        return config["lcss"]["channels"]["welcome"]

    @staticmethod
    def lcss_identification() -> int:
        return config["lcss"]["channels"]["identification"]
    
    @staticmethod
    def lcss_rules() -> int:
        return config["lcss"]["channels"]['rules']

    @staticmethod
    def lcss_counting() -> int:
        return config["lcss"]["channels"]["counting"]

    @staticmethod
    def log_dms() -> int:
        return config["log"]["channels"]["dms"]

    @staticmethod
    def log_logs() -> int:
        return config["log"]["channels"]["logs"]

    @staticmethod
    def role_botperms() -> int:
        return config["roles"]["botperms"]