# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json


class Parser(object):
    def __init__(self):
        self.__DEFAULT_SOUP_PARSER = "lxml"
        self.__DEFAULT_USER_ELEMENT = (
            "input", {"name": "userid", "type": "hidden"})

    @staticmethod
    def extract_info_value(item_in):
        return item_in.find('div', class_='num')[
            "title"].replace(',', '')

    @staticmethod
    def get_followers(profile_soup):
        item_followers = profile_soup.find("div", class_="item_followers")
        return Parser.extract_info_value(item_in=item_followers)

    @staticmethod
    def get_followings(profile_soup):
        item_followings = profile_soup.find("div", class_="item_following")
        return Parser.extract_info_value(item_in=item_followings)

    @staticmethod
    def get_counts_of_posts(profile_soup):
        item_posts = profile_soup.find("div", class_="item_posts")
        return Parser.extract_info_value(item_in=item_posts)

    @staticmethod
    def get_introduction(profile_soup):
        user_info_list = []
        user_info = profile_soup.find("div", class_="info")
        user_info = user_info.find("div", class_="sum")
        for each_info in user_info:
            if each_info.text != ' ':
                user_info_list.append(str(each_info.text))
        return user_info_list

    def get_soup(self, response):
        soup = BeautifulSoup(response.text, self.__DEFAULT_SOUP_PARSER)
        return soup
    
    def get_userid(self, profile_soup):
        userid_input_element = profile_soup.find(
            "input", {"name": "userid",
                      "type": "hidden"})
        if userid_input_element:
            return userid_input_element["value"]
        return ""

    def get_maxid(self, response):
        maxid = json.loads(response.text)["posts"]["maxid"]
        return maxid

    def get_userid_and_soup(self, response):
        soup = BeautifulSoup(response.text, self.__DEFAULT_SOUP_PARSER)
        userid_input_element = soup.find("input", {"name": "userid",
                                                   "type": "hidden"}
                                         )

        if userid_input_element:
            return userid_input_element["value"], soup

        return "", ""
    

class ApiParser(object):
    def __init__(self) -> None:
        pass

    def get_maxid(self, scraped_api_data:dict) -> str:
        return scraped_api_data["posts"]["maxid"]