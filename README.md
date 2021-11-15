# Html Meta Data Parse

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://github.com/timothycrosley/isort)
[![bandit](https://github.com/PyCQA/bandit/workflows/Build%20and%20Test%20Bandit/badge.svg)](https://github.com/PyCQA/bandit)
[![PyPI version](https://badge.fury.io/py/pip.svg)](https://badge.fury.io/py/pip)

# About
[html-meta-data-parse](https://pypi.org/project/html-meta-data-parse/), collects metadata from URL, or HTML content.


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

### Test
```bash
$ make test
```

### Install
```bash
pip install html-meta-data-parse
```

### Example
```bash
from html_meta_data_parse import HtmlMetaDataParse
html_meta_data_parse = HtmlMetaDataParse()
html_meta_data_parse.get_meta_data_by_url('https://example.com/')

>>> html_meta_data_parse.get_meta_data_by_url("https://www.pcmag.com/news/cloudflare-mitigates-nearly-2-tbps-ddos-attack")
{
  'title': 'Cloudflare Mitigates Nearly 2 Tbps DDoS Attack',
  'image': 'https://i.pcmag.com/imagery/articles/00NczM1wpOM7qFzLIwNp6XG-1.fit_lim.size_1200x630.v1636923971.jpg',
  'content': 'The attack was reportedly launched from approximately 15,000 devices.',
  'type': 'article',
  'twitter_handle': '@pcmag',
  'site_name': 'PCMAG',
  'url': 'https://www.pcmag.com/news/cloudflare-mitigates-nearly-2-tbps-ddos-attack'
}

>>> html_meta_data_parse.get_meta_data_by_url("https://www.cnet.com/tech/mobile/how-the-covid-19-pandemic-shaped-samsungs-new-galaxy-phone-update-launching-today/")
{
  'author': 'https://www.facebook.com/cnet',
  'title': 'Samsung knows the pandemic changed tech, so Galaxy phones are changing too',
  'image': 'https://www.cnet.com/a/img/h15nl2OCT89fWO9h_-Jza3vf5w8=/0x0:4000x2667/1200x630/right/top/2021/01/20/249ee601-c66f-48c2-84c2-fbc7d1606c61/109-samsung-galaxy-s21-and-s21-ultra-comparison.jpg',
  'content': "The company's decisions were affected by our evolving relationship with our phones.",
  'type': 'article',
  'twitter_handle': '@CNET',
  'site_name': 'CNET',
  'url': 'https://www.cnet.com/tech/mobile/how-the-covid-19-pandemic-shaped-samsungs-new-galaxy-phone-update-launching-today/'
}

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
#### Increment version in setup.py
```bash
$ make deploy STAGE=testpypi # test

$ make deploy STAGE=pypi # public
```


## Authors

* **Immanuel George** - *Initial work*
