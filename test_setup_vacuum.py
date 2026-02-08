import unittest
from unittest.mock import patch, MagicMock
import setup_vacuum

class TestSetupVacuum(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'BASE_URL': 'http://test:8123/api',
            'HEADERS': {'Auth': 'Bearer test'},
            'ENTITY_ID': 'vacuum.test'
        }

    @patch('requests.get')
    def test_check_ha_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'components': ['xiaomi_miot']}
        mock_get.return_value = mock_response
        
        self.assertTrue(setup_vacuum.check_ha(self.config))

    @patch('requests.get')
    def test_check_device_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'state': 'idle', 'attributes': {'model': 'b106bk'}}
        mock_get.return_value = mock_response
        
        self.assertTrue(setup_vacuum.check_device(self.config))

    @patch('setup_vacuum.open', unittest.mock.mock_open())
    def test_generate_yaml(self):
        self.assertTrue(setup_vacuum.generate_yaml(self.config, ['10', '11']))

if __name__ == '__main__':
    unittest.main()
