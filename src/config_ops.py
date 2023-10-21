import xml.etree.ElementTree as ET

from flask import g

class ConfigExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app, config_path=None):
        if config_path is None:
            self.base_dir = load_base_dir()
        else:
            self.base_dir = load_base_dir(config_path)
            
        @app.before_request
        def base_dir():
            g.base_dir = self.base_dir

def make_config(args, config_path = 'config.xml'):
    base_dir = args['base_dir']
    if not base_dir:
        raise ValueError('base directory must be present')
    
    tree = make_tree()
    root = tree.getroot()
    set_key('base_dir', base_dir, tree)
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
        tree = ET.fromstring(data)
        base_dir = tree.findtext('base_dir')
        return base_dir