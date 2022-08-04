from utils.paddle_scraper import PaddleScraper
from sqlalchemy import create_engine
import pandas as pd
import json

if __name__ == '__main__':
    with open('credentials.json') as cred:
        credentials = json.load(cred)
    RDS_HOST = credentials['RDS_HOST']
    RDS_PASSWORD = credentials['RDS_PASSWORD']
    RDS_PORT = credentials['RDS_PORT']

    # Retrieve all new data
    bot = PaddleScraper(headless=True)
    player = bot.search_player('Candido Jorge Alfaro')
    new_candido_info = bot.get_info()

    # Retrieve existing data
    print("connecting to the database")
    engine = create_engine(f'postgresql+psycopg2://postgres:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/paddle')
    old_candido_info = pd.read_sql_table('candido_info', engine)
    # Compare both tables and drop the duplicates
    merged_dfs = pd.concat([old_candido_info, new_candido_info])
    merged_dfs = merged_dfs.drop_duplicates(keep=False)
    merged_dfs.to_sql('candido_info', engine, if_exists='append', index=False)
    print("Done, have a nice day!")

