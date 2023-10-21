from .config import *

class ConfigExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app, config_path=None):
        if config_path is None:
            self.base_dir = load_base_dir()
        else:
            self.base_dir = load_base_dir(config_path)

        if not Path(self.base_dir).is_dir():
            raise ValueError("'%s' does not exist or is not directory" % self.base_dir)

        @app.before_request
        def base_dir():
            g.base_dir = self.base_dir