import unittest
from unittest.mock import patch, MagicMock, mock_open
import setup_vacuum


class TestSetupVacuum(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'BASE_URL': 'http://test:8123/api',
            'HEADERS': {'Authorization': 'Bearer test'},
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
    def test_check_ha_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection failed")
        self.assertFalse(setup_vacuum.check_ha(self.config))

    @patch('requests.get')
    def test_check_device_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'state': 'idle', 'attributes': {'model': 'b106bk'}}
        mock_get.return_value = mock_response
        
        self.assertTrue(setup_vacuum.check_device(self.config))

    @patch('requests.get')
    def test_check_device_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        self.assertFalse(setup_vacuum.check_device(self.config))

    @patch('builtins.open', mock_open())
    def test_generate_yaml(self):
        result = setup_vacuum.generate_yaml(self.config, ['10', '11'])
        self.assertTrue(result)

    def test_parse_vevs_log(self):
        log = '{"out":["[\\"1_12_1_3_2_1_1_0\\",\\"1_10_1_3_2_1_1_1\\"]"]}'
        result = setup_vacuum.parse_vevs_log(log)
        self.assertEqual(result, ['10', '12'])

    def test_get_config(self):
        with patch.dict('os.environ', {
            'HASS_HOST': '192.168.1.1',
            'HASS_TOKEN': 'test_token',
            'ENTITY_ID': 'vacuum.test'
        }):
            config = setup_vacuum.get_config()
            self.assertEqual(config['BASE_URL'], 'http://192.168.1.1:8123/api')
            self.assertIn('Authorization', config['HEADERS'])


if __name__ == '__main__':
    unittest.main()
