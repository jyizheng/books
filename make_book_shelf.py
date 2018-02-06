# -*-encoding: utf-8 -*-
import os 
import sys
import logging
import urllib
import json
import re



logging.basicConfig(tream=sys.stdout, level=logging.INFO)

LOG = logging.getLogger(__name__)

ROOT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
GITHUB_LINK = "https://github.com/yowenter/books"

LOG.info("Root Directory: %s", ROOT_DIRECTORY)

HeaderLine = """
# Books

```
The books list here mainly contains economics, technology, mind and psychology.
I've read them more than once.
They introduce different insights about the world and self.
Hope you'll find interest in them.  - TAOG
```
"""

class Book(object):
    path_pattern = r".*\.(pdf)"
    attributes = [
        "name",
        "path",
        "download_link",
        "tags",
        "category",
        "goodread_link",
        "douban_link"
    ]

    md_attributes = [
        "name",
        "md_download_link"
    ]
    read_only_attributes = [
        "name",
        "download_link"
    ]
    
    def __init__(self, **kwargs):
        for attr  in self.attributes:
            if kwargs.get(attr) and attr not in self.read_only_attributes:
                setattr(self, attr, kwargs[attr])


    @property
    def name(self):
        fname = os.path.split(self.path)[-1]
        slices = fname.split('.')
        if len(slices) > 1:
        	return "".join(slices[:-1])
        else:
        	return slices[0]


    @property
    def download_link(self):
        return "{}/blob/master{}".format(GITHUB_LINK, urllib.quote(self.path.encode("utf-8")))

    @property
    def md_download_link(self):
        return "[{}]({})".format(self.download_link, self.download_link)
    
    def md_column(self):
        return "| {} |\n".format(" | ".join([getattr(self, a, "None").encode('utf-8') for a in self.md_attributes]))


    @classmethod
    def md_column_header(cls):
        title_1_line = "| {} |".format(" | ".join(["%20s"%c for c in cls.md_attributes]))
        title_2_line = "| {} |".format(" | ".join([ "-"*20 for c in cls.md_attributes]))
        return "{}\n{}\n".format(title_1_line, title_2_line)
    



    
    

class MetaData(object):
    def __init__(self, path):
        fpath = os.path.join(ROOT_DIRECTORY, path)
        assert os.path.exists(fpath)
        with open(fpath, "r") as f:
            LOG.info("Loading metadata from `%s`", fpath)
            data = json.load(f)

            self.data = data

    
    def find_all_book(self):
        for d in self.data:
            LOG.debug("Loading book source data `%s`", d)
            book = Book(**d)
            yield book

        


if __name__ == '__main__':
    book_files = list()
    for root, _, files in os.walk(ROOT_DIRECTORY):
        if len(_)>0:
            continue
        for f in files:
            if not re.match(Book.path_pattern, f):
                continue
            path = os.path.join(root, f)[len(ROOT_DIRECTORY):]
            book_files.append({"path":path, "name":Book(path=path).name})
    
    with open(os.path.join(ROOT_DIRECTORY,"tmp_metadata.json"), "w") as f:
        LOG.info("Output tmp metadata file.")
        f.write(json.dumps(book_files))

        





    metadata = MetaData("metadata.json")
    books = list(metadata.find_all_book())

    readme_path = os.path.join(ROOT_DIRECTORY, "README.md")
    print "Output Readme: %s"%readme_path
    if os.path.exists(readme_path):
    	os.system("rm %s"%readme_path)
    with open(readme_path,"w") as f:
    	f.write(HeaderLine)
        f.write(Book.md_column_header())
        for b in books:
            f.write(b.md_column())


    
            
            
            
        
        



        
    



