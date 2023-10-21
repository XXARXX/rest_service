import unittest
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

import src.config_ops as conf

class ConfigTest(unittest.TestCase):
    def test_create_config(self):
        valid_config = "<?xml version='1.0' encoding='UTF-8'?>\n<config><base_dir>test dir</base_dir></config>"

        with TemporaryDirectory() as tempdir:
            config_path = '%s\\%s' % (tempdir, 'conf.ini')
            conf.make_config({'base_dir': 'test dir'}, config_path)
            with open(config_path) as f:
                data = f.read()
                self.assertEqual(data, valid_config)
    
    def test_add_key(self):
        valid_tree = b"<config><test>test value</test><test2>test value 2</test2></config>"

        tree = conf.make_tree()
        conf.add_key('test', 'test value', tree)
        conf.add_key('test2', 'test value 2', tree)
        conf.add_key('test', 'test value 2', tree)
        self.assertEqual(ET.tostring(tree.getroot()), valid_tree)

    def test_set_key(self):
        valid_tree = b"<config><test>test value 2</test><test2>test value 2</test2></config>"

        tree = conf.make_tree()
        conf.set_key('test', 'test value', tree)
        conf.set_key('test2', 'test value 2', tree)
        conf.set_key('test', 'test value 2', tree)
        self.assertEqual(ET.tostring(tree.getroot()), valid_tree)

    def test_make_tree(self):
        valid_tree = b"<config />"

        tree = conf.make_tree()
        self.assertEqual(ET.tostring(tree.getroot()), valid_tree)

    def test_load_base_dir(self):
        config_name = 'config.xml'
        valid_base_dir = 'C:\\test\\base directory'
        tree = '<config><base_dir>%s</base_dir></config>' % valid_base_dir
        
        with TemporaryDirectory() as tempdir:
            config_path = "%s\\%s" % (tempdir, config_name)
            with open(config_path, 'w') as f:
                f.write(tree)
            base_dir = conf.load_base_dir(config_path)
            self.assertEqual(valid_base_dir, base_dir)