# -*-encoding: utf-8 -*-

import os 

ROOT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

GITHUB_LINK = "https://github.com/yowenter/books"

README_PATH = os.path.join(ROOT_DIRECTORY, "README.md")

METADATA_JSON_PATH = os.path.join(ROOT_DIRECTORY,"metadata.json")


HeaderLine = """
# Books

```
The books list here mainly contains economics, technology, mind and psychology.
I've read them more than once.
They introduce different insights about the world and self.
Hope you'll find interest in them.  - TAOG
```


"""
FooterLine = """

## README

-  `pip install requests`
-  `python library/shelf.py`

## PR

Any suggestions or pull requests are welcome. 

## TODO

- [ ] ADD DouBan Link
- [ ] ADD GoodRead Link
- [ ] ADD Shanghai Library Link
- [ ] ADD Recommend
- [ ] ADD Export to Excel/Google Docs/Airtable



"""