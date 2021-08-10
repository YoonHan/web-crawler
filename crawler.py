from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


class Crawler():

    def __init__(self):
        pass

    @staticmethod
    def get_html_text(url='', headers=None):
        try:
            res = requests.get(url, headers=headers)
        except Exception as e:
            print('[Error]', e)
        return res.text

    def parse_html(self, html_str):
        bs = BeautifulSoup(html_str, 'html.parser')
        return bs

