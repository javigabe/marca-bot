import collections
import logging
import requests
import time

from bs4 import BeautifulSoup


MarcaResult = collections.namedtuple('MarcaResult', 'link title')


class MarcaParser(object):
    def __init__(self):
        r = requests.get('https://marca.com/', timeout=5)
        self.tree = BeautifulSoup(r.text, 'html.parser')

    def heading(self):
        full_title_page = self.tree.find(id='portada')

        title_page = full_title_page \
            .find(class_='row-layout') \
            .find(class_='content-item') \
            .article

        link = title_page.find('a').attrs['href']
        article_name = title_page.header.h2.a.text

        return MarcaResult(title=article_name, link=link)


class MarcaChecker(object):

    def __init__(self, time_to_sleep=10):
        self.last_heading = MarcaResult(link='', title='')
        self.time_to_sleep = time_to_sleep

    def run_until_update_detected(self):
        while True:
            try:
                new_heading = MarcaParser().heading()

                if new_heading.link != self.last_heading.link:
                    self.last_heading = new_heading
                    return new_heading

                logging.info('No updates found, sleeping...')
            except Exception:
                logging.exception('Error creating request to marca')

            time.sleep(self.time_to_sleep)
