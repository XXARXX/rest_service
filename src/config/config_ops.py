import xml.etree.ElementTree as ET
from pathlib import Path

from flask import g

class ConfigError(Exception):
    pass

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

def make_config(args, config_path = 'config.xml'):    
    tree = make_tree()
    root = tree.getroot()
    for k, v in args.items():
        set_key(k, v, tree)
    tree.write(config_path, encoding='UTF-8', xml_declaration=True)

def make_tree():
    root = ET.Element('config')
    tree = ET.ElementTree(root)
    return tree

def add_key(key, value, tree):
    root = tree.getroot()
    elem = root.find(key)
    if elem is None:
        elem = ET.SubElement(root, key)
        elem.text = value

def set_key(key, value, tree):
    root = tree.getroot()
    elem = root.find(key)
    if elem is None:
        elem = ET.SubElement(root, key)
    elem.text = value

def load_base_dir(config_path = 'config.xml'):
    with open(config_path) as f:
        data = f.read()
        try:
            tree = ET.fromstring(data)
        except ET.ParseError as e:
            raise ConfigError('invalid config file: %s' % e)
        base_dir = tree.findtext('base_dir')
        if base_dir is None:
            raise ConfigError('invalid config file')
        return base_dir