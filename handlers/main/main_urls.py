#coding=utf-8

from main_handler import MainHandler
from handlers.account.account_urls import account_urls

handlers = [
    (r'/',MainHandler)
]

handlers += account_urls