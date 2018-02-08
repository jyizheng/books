# -*-encoding: utf-8 -*-

import os 
import abc 
import logging
import json 
import requests
import csv
import re 
from utils import to_unicode

LOG = logging.getLogger(__name__)



def lcs(a, b):
    #todo
    return []


            



def txt_similarity(s1, s2):
    us1 = to_unicode(s1)
    us2 = to_unicode(s2)
    us1 = "".join(re.findall(u"[\u4e00-\u9fa5]|\w",us1)).lower()
    us2 = "".join(re.findall(u"[\u4e00-\u9fa5]|\w",us2)).lower()
    return len(lcs(us1, us2))




class Shelf(object):
    def __init__(self, books):
        self.books = books

    
    def add_book(self, book):
        if not getattr(book, "name", None):
            LOG.info("Book has no name %s", book)
            return None 
        similarity = 0
        index = None 
        for idx, b in enumerate(self.books):
            sim = txt_similarity(book.name, b.name)
            if sim>similarity:
                index = idx
                similarity = sim
        
        if similarity>4:
            LOG.info("UPDATE Book %s",book)
            self.books[index].update(**book.as_dict())
        else:
            LOG.info("ADD Book %s", book)
            self.books.append(book)

    def __repr__(self):
        return str(self.books)
    


class Book(object):
    path_pattern = r".*\.(pdf)"
    
    attributes = [
        "name",
        "path",
        "tags",
        "category",
        "goodread_link",
        "douban_link"
    ]

    def __init__(self, **kwargs):
        self.update(**kwargs)
    
    def update(self, **kwargs):
        for attr in self.attributes:
            if kwargs.get(attr):
                setattr(self, attr, kwargs[attr])
    

    @property
    def filename(self):
        fname = os.path.split(getattr(self, "path", ""))[-1]
        slices = fname.split('.')
        if len(slices) > 1:
        	return "".join(slices[:-1])
        else:
        	return slices[0]
    
    @property
    def parent(self):
        fname = os.path.split(getattr(self, "path", ""))
        if len(fname)>=2:
            parent  = fname[-2]
            return parent 
        else:
            return None


    
    def __repr__(self):
        return str({k:getattr(self,k,None) for k in self.attributes})



class BookReader(object):
    # __metaclass__ = abc.ABCMeta
    
    def __init__(self, fpath):
        assert os.path.exists(fpath)
        self.fpath = fpath

    def read(self):
        raise NotImplementedError


class CSVBookReader(BookReader):
    
    def read(self):
        with open(self.fpath, "r") as f:
            csv_reader  = csv.reader(f)
            header = next(csv_reader)

            for row in csv_reader:
                yield dict(zip(header, row))
            

class JSONBookReader(BookReader):
    
    def read(self):
        with open(self.fpath, "r") as f:
            LOG.info("Loading data from `%s`", self.fpath)
            data = json.load(f)

        return (d for d in data)
    
    
class AirtableBookReader(BookReader):
    
    def __init__(self, api_key, api):
        self.api_key = api_key
        self.api = api
    
    def fetch_records(self):
        resp = requests.get(self.api, headers= {"Authorization":"Bearer {}".format(self.api_key)}, timeout=10)
        return resp.json()

    def read(self):
        records = self.fetch_records().get("records")

        for r in records:
            data = r['fields']
            d = {"_".join(k.lower().split(" ")):data[k] for k in data }
            yield d


        







