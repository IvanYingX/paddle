from utils.paddle_scraper import PaddleScraper
from sqlalchemy import create_engine
import pandas as pd


if __name__ == '__main__':
    # Retrieve all new data
    bot = PaddleScraper(headless=True)
    player = bot.search_player('Candido Jorge Alfaro')
    new_candido_info = bot.get_info()

    # Retrieve existing data
    print("connecting to the database")
    engine = create_engine('postgresql+psycopg2://postgres:AiCore2022@paddle.cnrx3vj42weu.eu-west-1.rds.amazonaws.com:5432/paddle')
    old_candido_info = pd.read_sql_table('candido_info', engine)
    # Compare both tables and drop the duplicates
    merged_dfs = pd.concat([old_candido_info, new_candido_info])
    merged_dfs = merged_dfs.drop_duplicates(keep=False)
    merged_dfs.to_sql('candido_info', engine, if_exists='append', index=False)