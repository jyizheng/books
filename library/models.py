# -*-encoding: utf-8 -*-

import os 
import abc 
import logging
import json 
import requests
import csv
import re 
from utils import to_unicode, to_str

LOG = logging.getLogger(__name__)





def lcs(a, b):
    def pprint(matrix):
        for row in matrix:
            LOG.debug(row)

    #todo

    matrix = [[0 for i in range(len(b))] for j in range(len(a))]
    # symbols =  [['' for i in range(len(b))] for j in range(len(a))]

    if a[0] == b[0]:
        matrix[0][0] = 1 

    for i in range(1,len(a)):
        for j in range(1,len(b)):

            if a[i]==b[j]:
                matrix[i][j] = matrix[i-1][j-1] +1 
            else:
                matrix[i][j] = max(matrix[i][j-1], matrix[i-1][j])
            
            pprint(matrix)

    pprint(matrix)
    
    return matrix[len(a)-1][len(b)-1]

    



            



def txt_similarity(s1, s2):
    
    us1 = to_unicode(s1)
    us2 = to_unicode(s2)
    us1 = "".join(re.findall(u"[\u4e00-\u9fa5]|\w",us1)).lower()
    us2 = "".join(re.findall(u"[\u4e00-\u9fa5]|\w",us2)).lower()
    ls = lcs(us1, us2)
    # LOG.info("%s vs %s, %s, %s",to_str(s1), to_str(s2), ls, ls/float(len(us1)))
    return ls/float(len(us1))




class Shelf(object):
    def __init__(self, books):
        self.books = books

    
    def add_book(self, book, check_similarity=False):
        if not getattr(book, "name", None):
            LOG.info("Book has no name %s", book)
            return None 
        
        if not check_similarity:
            found = False
            for idx, b in enumerate(self.books):
                if b.name == book.name:
                    LOG.info("UPDATE Book old: %s new: %s", b, book)
                    self.books[idx].update(**book.as_dict())
                    found = True
                    break
            if not found:
                LOG.info("ADD Book %s", book)
                self.books.append(book)
            return book
                

        similarity = 0
        index = None 
        old_book = None 
        for idx, b in enumerate(self.books):
            sim = txt_similarity(book.name, b.name)
            if sim>similarity:
                index = idx
                similarity = sim
                old_book = b
        
        if similarity>0.8:
            LOG.info("Similarity > 0.8, UPDATE Book old: %s new: %s", old_book, book)
            self.books[index].update(**book.as_dict())
        else:
            LOG.info("Similarity < 0.8, ADD Book %s", book)
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
        "goodread",
        "douban"
    ]

    def __init__(self, **kwargs):
        self.update(**kwargs)
    
    def update(self, **kwargs):
        for attr in self.attributes :
            if kwargs.get(attr) is not None:
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
        return to_str(getattr(self, "name", ""))
    


    def as_dict(self):
        return {k:getattr(self, k, None) for k in self.attributes}


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

            d = {to_str("_".join(k.strip().lower().split(" "))):to_str(data[k]) for k in data }
            yield d


        







