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

1,  `pip install requests`
2,  `python library/shelf.py`

## PR

Any suggestions or pull requests are welcome. 



"""