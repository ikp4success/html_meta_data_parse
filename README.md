# Html Meta Data Parse

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://github.com/timothycrosley/isort)
[![bandit](https://github.com/PyCQA/bandit/workflows/Build%20and%20Test%20Bandit/badge.svg)](https://github.com/PyCQA/bandit)

# About
HtmlMetaDataParse, collects meta data from url, or html content.


# Usage
#### Python Version: 3.8+

### Setup

```bash
$ make .venv
$ make clean # cleans virtual environment folder
```
Setup virtual environment

### Pre-commit

[pre-commit](https://pre-commit.com/) installed automatically via .venv, used for linting best practices.

```bash
$ make pre-commit
```
# test
```bash
$ make test
```

```bash
from html_meta_data_parse import HtmlMetaDataParse
html_meta_data_parse = HtmlMetaDataParse()
html_meta_data_parse.get_meta_data_by_url(https://example.com/)

import requests
res = requests.get("https://example.com/")
html_meta_data_parse.get_meta_data_by_html(res.text)


html_meta_data_parse = HtmlMetaDataParse(url="https://example.com/", proxy=<proxy_dict>)
html_meta_data_parse.get_meta_data_by_url()
```
#### Attributes
* url
* html_text
* override_meta_keys
* proxy (http://2.python-requests.org/en/master/user/advanced/?highlight=proxies#proxies)


#### Functions
```
# url is required
html_meta_data_parse.get_meta_data_by_url(url)

# html_text is required
html_meta_data_parse.get_meta_data_by_html(html_text=html_text)
```

##### Override Meta Keys
HtmlMetaDataParse uses a predefined set of keys to parse meta data from html content. However it also provides an option to override meta keys of your choice.

```

html_meta_data_parse.get_meta_data_by_url(
  url,
  override_meta_keys
 )


html_meta_data_parse.get_meta_data_by_html(
  html_text,
  override_meta_keys,
)

#meta_keys_sample
meta_keys = {
        "author": {
            "name": [
                "author"
            ],
            "property": [
                "bt:author",
                "article:publisher",
                "dcterms.creator"
            ],
            "itemprop": [
                "author",
            ]

        },

        "title": {
            "name": [
                "title",
                "dcterms.title",
                "",
                "twitter:title"
            ],
            "property": [
                "og:title"
            ],
            "itemprop": [
                "title",
            ]
        },

        "image": {
            "name": [
                "image",
                "twitter:image",
                "thumbnail"
            ],
            "property": [
                "og:image"
            ],
            "itemprop": [
                "image",
            ]
        },

        "content": {
            "name": [
                "description",
                "twitter:description",
                "twitter:image:alt"
            ],
            "property": [
                "og:description",
                "og:image:alt"
            ],
            "itemprop": [
                "description",
            ]
        }
   }

```

# Deploy
Increment version in setup.py
```bash
$ make deploy STAGE=testpypi # test

$ make deploy STAGE=pypi # public
```


## Authors

* **Immanuel George** - *Initial work*
