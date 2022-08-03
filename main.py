from utils.scraper import PaddleScraper
import time

if __name__ == '__main__':
    bot = PaddleScraper()
    player = bot.search_player('Candido Jorge Alfaro')
    time.sleep(10)