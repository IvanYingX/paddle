import unittest
from unittest.mock import patch, Mock, call
from paddle_scraper import PaddleScraper
import sys

class TestPaddleScraper(unittest.TestCase):

    def setUp(self):
        self.obj_scraper = PaddleScraper(False)

    
    @patch('paddle_scraper.PaddleScraper.accept_cookies')   
    @patch('paddle_scraper.PaddleScraper.find_elements_in_container')  
    @patch('time.sleep')  
    def test_search_all_players(self,   
        mock_sleep: Mock,
        mock_container: Mock,   
        mock_cookies: Mock
        ):
        self.obj_scraper.launch_page('https://www.worldpadeltour.com/jugadores/?ranking=masculino')
        self.obj_scraper.search_all_players()
        mock_cookies.assert_called_once()
        cookies_call_count = mock_cookies.call_count
        mock_container.assert_called_once_with(xpath_container='//*[@id="site-container"]/div[4]/div/div[1]/ul',
            tag_elements='li'
            )
        mock_sleep.assert_has_calls(calls=[call(1), call(4)], any_order=True)
        self.assertEqual(cookies_call_count, 1)

    @patch('builtins.input', return_value='Blair')
    def test_get_input(self, mock_input: Mock):
        self.obj_scraper.get_input()
        mock_input.assert_called()  
        self.assertEqual(mock_input.return_value, 'Blair')

    
    def tearDown(self):
        self.obj_scraper.driver.quit()
        del self.obj_scraper

if __name__ == '__main__': 
    unittest.main(argv=[''], verbosity=2, exit=True)



