#!/usr/bin/env python

import logging

import telegram
import marca
import os

class TelegramBot(object):

    def __init__(self, chat_id, token):
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=token)

    def run(self):
        mu = marca.MarcaChecker()
        logging.info('Running bot...')

        while True:
            result = mu.run_until_update_detected()
            logging.info('New heading detected: {}'.format(result))
            self.bot.send_message(chat_id=self.chat_id, text=result.title)


if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO)

    token = os.getenv("MARCA_TOKEN")
    bot = TelegramBot(415279177, token)
    bot.run()
