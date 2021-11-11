from bs4 import BeautifulSoup
from parsel import SelectorList


def format_to_fine_content(content_list_selector):
    if isinstance(content_list_selector, SelectorList):
        content_list_selector = content_list_selector.extract()

    content_bs = BeautifulSoup("".join(content_list_selector))
    if content_bs:
        for cbs in content_bs(['script', 'style', 'meta', 'noscript']):
            cbs.decompose()
        fine_content = content_bs.stripped_strings
        fmc = format_content_list(fine_content).strip()
        return fmc


def format_content_list(content_list):
    if isinstance(content_list, SelectorList):
        content_list = content_list.extract()
    content = ""
    for con in content_list:
        if con:
            content += "{} ".format(con.strip())

    return content


def get_meta_data_keys():
    return {
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
        },

        "media": {
            "name": [
                "video",
            ],
            "property": [
                "og:video",
                "og:video:secure_url"
            ],
            "itemprop": [
                "video",
            ]
        },

        "audio": {
            "name": [
                "audio",
            ],
            "property": [
                "og:audio",
                "og:audio:secure_url"
            ],
            "itemprop": [
                "audio",
            ]
        },

        "pubdate": {
            "name": [
                "lastmod",
                "pubdate",
                "pubDate"
            ],
            "property": [
                "og:pubdate",
                "bt:modDate",
                "bt:pubDate",
                "article:published_time",
                "article:modified_time",
                "dcterms.modified",
                "dcterms.date"
            ],
            "itemprop": [
                "dateModified",
                "dateCreated",
                "datePublished",
            ]
        },

        "type": {
            "name": [
                "type"
            ],
            "property": [
                "og:type"
            ],
        },

        "twitter_handle": {
            "name": [
                "twitter:site"
            ],
            "property": [
                "og:twitter:site"
            ],
            "itemprop": [
                "twitter:site",
            ]
        },

        "site_name": {
            "name": [
                "site_name"
            ],
            "property": [
                "og:site_name"
            ],
        },
        "url": {
            "name": [
                "url"
            ],
            "property": [
                "og:url"
            ],
        }
    }
