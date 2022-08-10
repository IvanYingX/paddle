from tkinter import N
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class Scraper:
    
    def __init__(self, headless: bool):
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def launch_page(self, webpage_address: str):
        self.driver.get(webpage_address)
        return self.driver.current_url

    def click_element(self, xpath: str):
        '''
        Finds and clicks the "Accept" cookies button

        Parameters
        ----------
        xpath: str
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
        self.click_element(xpath) == True


    def find_elements_in_container(self,
                                   xpath_container: str,
                                   tag_elements: str,
                                   direct_child: bool = True) -> list:
        '''
        Finds a container and returns a list of elements inside it

        Parameters
        ----------
        xpath_container: str
            The Xpath of the container
        tag_elements: str
            The tag of the elements to be found
        direct_child: bool
            If True, the elements will be found directly inside the container,
            otherwise, they will be found inside the container's children
        '''                                   

        container = self.driver.find_element(By.XPATH, xpath_container)
        if direct_child:
            elements_in_container = container.find_elements(By.XPATH, f'./{tag_elements}')
        else:
            elements_in_container = container.find_elements(By.XPATH, f'.//{tag_elements}')

        return elements_in_container


if __name__ == '__main__':
    pass