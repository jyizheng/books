# -*-encoding: utf-8 -*-

import os 
import abc 
import logging
import json 
import csv

LOG = logging.getLogger(__name__)

class Shelf(object):
    def __init__(self, books):
        self.books = books

    
    def add_book(self, book):
        if book.name not in [b.name for b in self.books]:
            self.books.append(book)
        
        else:
            index = None 
            for idx, b in self.books:
                if b.name == book.name:
                    index = idx
                    break

            del self.books[index]
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
    
    





