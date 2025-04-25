# -*- coding: utf-8 -*-
import json
import cloudscraper
from bs4 import BeautifulSoup


class PixwoxRequest(object):
    def __init__(self):
        self.__DEFAULT_SOUP_PARSER = "lxml"
        self.__scraper = cloudscraper.create_scraper(
            delay=10,
            browser={"custom": "ScraperBot/1.0",
                     "platform": "windows",
                     "mobile": "False"})

    def send_requests(self, url):
        response = self.__scraper.get(url)
        return response

    def get_init_content(self, username: str) -> str:
        get_url = f"https://www.picnob.com/zh-hant/profile/{username}"
        res = self.send_requests(get_url)
        soup = BeautifulSoup(res.text, self.__DEFAULT_SOUP_PARSER)
        userid_input_element = soup.find(
            "input", {"name": "userid", "type": "hidden"})

        if userid_input_element:
            return userid_input_element["value"], soup

        return "", ""
    
    def get_init_soup(self, profile_response):
        soup = BeautifulSoup(profile_response.text, self.__DEFAULT_SOUP_PARSER)
        return soup

    def get_maxid(self, response):
        maxid = json.loads(response.text)["posts"]["maxid"]
        return maxid

    def get_data(self, response):
        scraped_data = json.loads(response.text)
        return scraped_data
