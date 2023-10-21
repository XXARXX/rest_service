import unittest

from src.server import create_app
from src.config import make_config

class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        try:
            with open('config.xml', 'r') as f:
                self.original_config = f.read()
            make_config({'base_dir': 'testdata'})
        except:
            self.original_config = None

        self.client = create_app().test_client()

    @classmethod
    def tearDownClass(self):
        if self.original_config is None:
            return
        with open('config.xml', 'w') as f:
            f.write(self.original_config)

    def test_get_not_filtered_file(self):
        response = self.client.get('http://localhost:5000/api/show_file_content?filename=simpletestfile.txt')
        data = response.data.decode('utf-8')
        with open('testdata/simpletestfile.txt', 'r') as f:
            valid_data = f.read()
            self.assertEqual(data, valid_data)
    
    def test_get_filtered_file(self):
        valid_data = 'Raised when a local or global name is not found. This applies only to unqualified names. The associated value is an error message that includes the name that could not be found.\n'

        response = self.client.get('http://localhost:5000/api/show_file_content?filename=simpletestfile.txt&filter="Raised"')
        data = response.data.decode('utf-8')
        self.assertEqual(data, valid_data)

    def test_get_filtered_file2(self):
        valid_data = 'Raised when a local or global name is not found. This applies only to unqualified names. The associated value is an error message that includes the name that could not be found.\nThe name attribute can be set using a keyword-only argument to the constructor. When set it represent the name of the variable that was attempted to be accessed.\n'

        response = self.client.get('http://localhost:5000/api/show_file_content?filename=simpletestfile.txt&filter="The"')
        data = response.data.decode('utf-8')
        self.assertEqual(data, valid_data)