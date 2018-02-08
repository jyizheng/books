# -*-encoding: utf-8 -*-

import os 

ROOT_DIRECTORY = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

GITHUB_LINK = "https://github.com/yowenter/books"

README_PATH = os.path.join(ROOT_DIRECTORY, "README.md")

METADATA_JSON_PATH = os.path.join(ROOT_DIRECTORY,"metadata.json")

AIRTABLE_BOOK_CATALOG_API = os.getenv("AIRTABLE_BOOK_CATALOG_API", "https://api.airtable.com/v0/appQKS7QmJGB52PAi/Books")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")



HeaderLine = """
# Books

```
The books list here mainly contains economics, technology, mind and psychology.
I've read them more or less.
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

## More Info

Please visit my sharing airtable base [Book Catalog](https://airtable.com/shrhEVAegv3ifwlou) .
If you want to share your books, click [Join](https://airtable.com/invite/l?inviteId=inv1Z4cEG2JWQu8JR&inviteToken=25fb4f9dfc75e225adcc2c94e1d377a1d552b22e5e348cff89244e28cc592f75)

"""