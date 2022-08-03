from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

class Scraper:
    def __init__(self, url: str = 'https://www.worldpadeltour.com/'):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(url)

    def click_element(self, xpath: str):
        '''Candido Jorge Alfaro
            The Xpath of the element to be clicked
        '''
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()


    def accept_cookies(self, xpath: str = '//button[@id="c-p-bn"]'):
        '''
        Finds and clicks the "Accept" cookies button

        Parameters
        ----------
        xpath: str
            The Xpath of the Accept Cookies button
        '''
        self.click_element(xpath)


    def find_elements_in_container(self,
                                   xpath_container: str,
                                   tag_elements: str) -> list:

        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, f'./{tag_elements}')

        return elements_in_container

    

class PaddleScraper(Scraper):
    def search_player(self,
                      player: str,
                      xpath_search_bar: str = '//input[@class="c-form__control"]'):
        self.accept_cookies()
        time.sleep(1)
        self.click_element('//a[@title="Jugadores"]')
        search_bar = self.driver.find_element(By.XPATH, xpath_search_bar)
        search_bar.click()
        time.sleep(1)
        search_bar.send_keys(player)
        time.sleep(3)
        player_card = self.driver.find_element(By.XPATH, '//div[@class="c-ranking__block c-ranking__block--search"]')
        player_clickable = player_card.find_element(By.XPATH, './/a')
        player_clickable.click()

    def search_all_players(self):
        self.accept_cookies()
        time.sleep(1)
        self.click_element('//a[@title="Jugadores"]')
        players = self.find_elements_in_container(xpath_container='//*[@id="site-container"]/div[4]/div/div[2]/ul',
                                                  tag_elements='li')
        links = []
        for player in players:
            link = player.find_element(By.XPATH, './a').get_attribute('href')
            links.append(link)

        return links

    def get_info(self):
        table = self.driver.find_element(By.XPATH, '//div[@class="c-flex-table c-flex-table--ranking c-flex-table--blue is-visible"]')
        columns = table.find_elements(By.XPATH, './div')
        tournament = columns[0]
        # Get the data inside the tournament column
        tournament_list = self.retrieve_column_info(tournament)
        
        date = columns[2]
        date_list = self.retrieve_column_info(date)

        points = columns[3]
        points_list = self.retrieve_column_info(points)
        
        data_dict = {"Tournament": tournament_list,
                     "Date": date_list,
                     "Point": points_list}

        df_data = pd.DataFrame(data_dict)
        return df_data

    @staticmethod
    def retrieve_column_info(column):
        rows_container = column.find_element(By.XPATH, './ul')
        rows = rows_container.find_elements(By.XPATH, './li')
        data_list = []
        for row in rows:
            data = row.text
            data_list.append(data)

        return data_list
