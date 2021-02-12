import os

class BaseConfig:
    """Base configuration class"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CSRF_ENABLED = True
    CACHE_DEFAULT_TIMEOUT = 3600
    

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    
    DEBUG = True
    TEST_BINANCE_API_KEY = "OyAVMJsB9emzAmSfMazfcqVR6AraAlchCB0Te1KK6l8NaUok2Qttq8JuaVaL9wos"
    TEST_BINANCE_SECRET_KEY = "cU7DzFHQgdvOjgrOWeAXFMyMo5WXNU5Amx0fOJ1RJJ8WLXGfYOgCwthAFdUVR4yR"
    CACHE_TYPE = "filesystem"
    CACHE_DIR = "/tmp/cache"
    

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    
    CACHE_TYPE = "saslmemcached"
    CACHE_MEMCACHED_SERVERS = os.environ.get('MEMCACHIER_SERVERS', '').split(','),
    CACHE_MEMCACHED_USERNAME = os.environ.get('MEMCACHIER_USERNAME', ''),
    CACHE_MEMCACHED_PASSWORD = os.environ.get('MEMCACHIER_PASSWORD', ''),
    CACHE_OPTIONS = { 
        'behaviors': {
            # Faster IO
            'tcp_nodelay': True,
            # Keep connection alive
            'tcp_keepalive': True,
            # Timeout for set/get requests
            'connect_timeout': 2000, # ms
            'send_timeout': 750 * 1000, # us
            'receive_timeout': 750 * 1000, # us
            '_poll_timeout': 2000, # ms
            # Better failover
            'ketama': True,
            'remove_failed': 1,
            'retry_timeout': 2,
            'dead_timeout': 30
        }
    }
    
    
    
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}