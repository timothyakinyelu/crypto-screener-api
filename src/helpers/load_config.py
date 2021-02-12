from instance.config import BaseConfig, app_config

def loadConfig(MODE):
    try:
        if MODE == 'production':
            return app_config[MODE]
        else:
            return app_config[MODE]
    except ImportError:
        return BaseConfig