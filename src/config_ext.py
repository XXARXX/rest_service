from .config import *

class ConfigExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app, config_path=None):
        config = None
        if config_path is None:
            config = load_config()
        else:
            config = load_config(config_path)
        
        if 'base_dir' not in config:
            raise ConfigError("'base_dir not found in config")
        
        self.base_dir = config['base_dir']

        if not Path(self.base_dir).is_dir():
            raise ValueError("'%s' does not exist or is not directory" % self.base_dir)

        @app.before_request
        def base_dir():
            g.base_dir = self.base_dir