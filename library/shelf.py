# -*-encoding: utf-8 -*-

import os 
import logging
import re 
import json
import sys

logging.basicConfig(tream=sys.stdout, level=logging.INFO)

LOG = logging.getLogger(__name__)

from models import Book, Shelf, CSVBookReader, JSONBookReader, AirtableBookReader
from config import ROOT_DIRECTORY, README_PATH, METADATA_JSON_PATH, HeaderLine, FooterLine, AIRTABLE_API_KEY, AIRTABLE_BOOK_CATALOG_API
from render import ShelfMDRender, BookMDRender




def output_books_metadata():
    book_files = list()
    for root, _, files in os.walk(ROOT_DIRECTORY):
        if len(_)>0:
            continue
        for f in files:
            if not re.match(Book.path_pattern, f):
                continue
            path = os.path.join(root, f)[len(ROOT_DIRECTORY):]
            book_files.append({"path":path, "name":Book(path=path).filename.decode("utf-8")})
    
    with open(METADATA_JSON_PATH, "w") as f:
        LOG.info("Output  metadata file.")
        f.write(json.dumps(book_files))




def main():
    output_books_metadata()

    json_reader = JSONBookReader(METADATA_JSON_PATH)
    
    shelf = Shelf([])

    for d in json_reader.read():
        shelf.add_book(Book(**d))
    
    if AIRTABLE_API_KEY and AIRTABLE_BOOK_CATALOG_API:
        airtable_reader = AirtableBookReader(AIRTABLE_API_KEY, AIRTABLE_BOOK_CATALOG_API)
        for d in airtable_reader.read():
            shelf.add_book(Book(**d), check_similarity=True)



    LOG.info("Output readme %s", README_PATH)
    with open(README_PATH, "w") as f :
        f.write(HeaderLine)
        f.write(BookMDRender.md_header())
        for book in shelf.books:
            f.write(BookMDRender(book).md_column())
        
        f.write(FooterLine)
        





if __name__=='__main__':
    main()