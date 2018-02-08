# -*-encoding: utf-8 -*-

import urllib
from config import GITHUB_LINK

from utils import to_str

class BookMDRender(object):
    
    md_columns = [
        "channel",
        "name",
        "douban",
        "category"
    ]

    def __init__(self, book):
        self.book = book

    @property
    def name(self):
        return "[{}]({})".format(to_str(self.book.name), to_str(self.download_link))

    
    @property
    def channel(self):
        parent = self.book.parent
        link = "{}/blob/master{}".format(GITHUB_LINK, urllib.quote(to_str(parent.encode("utf-8"))))
        return "[{}]({})".format(parent.encode("utf-8"), link)

    @property
    def download_link(self):
        return "{}/blob/master{}".format(GITHUB_LINK, urllib.quote(self.book.path.encode("utf-8")))


    @classmethod
    def md_header(cls):
        title_1_line = "| {} |".format(" | ".join(["%20s"%c for c in cls.md_columns]))
        title_2_line = "| {} |".format(" | ".join([ "-"*20 for c in cls.md_columns]))
        return "{}\n{}\n".format(title_1_line, title_2_line)

    
    def md_column(self):
        return "| {} |\n".format(" | ".join([getattr(self, a, "") or getattr(self.book, a, "") for a in self.md_columns]))




class ShelfMDRender(object):
    def __init__(self, shelf):
        self.shelf = shelf


    
    def render_as_markdown(self):
        pass
        
