from src.neetcode_scraper import NeetCodeScraper
import json

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = NeetCodeScraper(data)
    bot.scrape_static_page()
    bot.scrape_dynamic_page()
    bot.write_2_csv()