import pytest

from html_meta_data_parse import HtmlMetaDataParse
from html_meta_data_parse.util import format_content_list, format_to_fine_content
from tests.util import build_html

test_meta_data_keys = {
    "author": {
        "name": ["author"],
        "property": ["bt:author", "article:publisher", "dcterms.creator"],
        "itemprop": ["author"],
    },
    "title": {
        "name": ["title", "dcterms.title", "", "twitter:title"],
        "property": ["og:title"],
        "itemprop": ["title"],
    },
    "image": {
        "name": ["image", "twitter:image", "thumbnail"],
        "property": ["og:image"],
        "itemprop": ["image"],
    },
    "content": {
        "name": ["description", "twitter:description", "twitter:image:alt"],
        "property": ["og:description", "og:image:alt"],
        "itemprop": ["description"],
    },
    "media": {
        "name": ["video"],
        "property": ["og:video", "og:video:secure_url"],
        "itemprop": ["video"],
    },
    "audio": {
        "name": ["audio"],
        "property": ["og:audio", "og:audio:secure_url"],
        "itemprop": ["audio"],
    },
    "pubdate": {
        "name": ["lastmod", "pubdate", "pubDate"],
        "property": [
            "og:pubdate",
            "bt:modDate",
            "bt:pubDate",
            "article:published_time",
            "article:modified_time",
            "dcterms.modified",
            "dcterms.date",
        ],
        "itemprop": ["dateModified", "dateCreated", "datePublished"],
    },
    "type": {"name": ["type"], "property": ["og:type"]},
    "twitter_handle": {
        "name": ["twitter:site"],
        "property": ["og:twitter:site"],
        "itemprop": ["twitter:site"],
    },
    "site_name": {"name": ["site_name"], "property": ["og:site_name"]},
    "url": {"name": ["url"], "property": ["og:url"]},
}


def headers():
    return {
        "Host": "test.com",
        "Accept": "/",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "test.com",
        "origin": "test.com",
        "DNT": "1",
        "Connection": "keep-alive",
    }


test_links = [
    "http://www.test-content-image.com/",
]


@pytest.fixture
def test_meta_data_keys_fixt():
    return test_meta_data_keys


@pytest.fixture
def build_html_fixt():
    def _method(html_dict_arr):
        return build_html(html_dict_arr)

    return _method


@pytest.fixture
def test_headers():
    return headers()


def test_html_meta_data_parse(test_meta_data_keys_fixt, build_html_fixt, requests_mock):
    html_meta_data_parse = HtmlMetaDataParse()
    assert test_meta_data_keys_fixt == html_meta_data_parse.meta_keys

    """ Name Attributes """
    html_dict_arr = [
        {"meta": {"attributes": {"content": "John Smith", "name": "author"}}},
        {"meta": {"attributes": {"content": "Loves the Water", "name": "description"}}},
        {"meta": {"attributes": {"content": "About John Smith", "name": "title"}}},
        {
            "meta": {
                "attributes": {
                    "content": "https://imageurl.com",
                    "name": "twitter:image",
                }
            }
        },
        {"meta": {"attributes": {"content": "https://videourl.com", "name": "video"}}},
        {"meta": {"attributes": {"content": "https://audiourl.com", "name": "audio"}}},
        {"meta": {"attributes": {"content": "01/10/2090", "name": "pubdate"}}},
        {"meta": {"attributes": {"content": "test article", "name": "type"}}},
        {"meta": {"attributes": {"content": "@test", "name": "twitter:site"}}},
        {"meta": {"attributes": {"content": "https://www.cnn.com/", "name": "url"}}},
        {"meta": {"attributes": {"content": "Site Name", "name": "site_name"}}},
    ]

    test_html = build_html_fixt(html_dict_arr)

    """By Html"""
    meta_data = html_meta_data_parse.get_meta_data_by_html(test_html)

    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]
    assert "test article" == meta_data["type"]
    assert "@test" == meta_data["twitter_handle"]
    assert "Site Name" == meta_data["site_name"]
    assert "https://www.cnn.com/" == meta_data["url"]

    alt_test_html = [
        {"meta": {"attributes": {"content": "https://altimgurl.com", "name": "image"}}}
    ]

    alt_test_html = build_html_fixt(alt_test_html)
    meta_data = html_meta_data_parse.get_meta_data_by_html(alt_test_html)
    assert "https://altimgurl.com" == meta_data["image"]

    alt_test_html2 = [
        {
            "head": {"child_arr": [{"title": {"body": "this is a title"}}]},
            "body": {"body": "this is a body"},
        }
    ]

    alt_test_html2 = build_html_fixt(alt_test_html2)
    meta_data = html_meta_data_parse.get_meta_data_by_html(alt_test_html2)

    assert "this is a title" == meta_data["title"]
    assert "this is a body" == meta_data["content"]

    alt_test_html3 = [{"body": {"body": "this is a body"}}]

    alt_test_html3 = build_html_fixt(alt_test_html3)
    meta_data = html_meta_data_parse.get_meta_data_by_html(alt_test_html3)
    assert "this is a body" == meta_data["content"]

    """By Url"""
    url = test_links[0]
    requests_mock.get(url, text=test_html)
    meta_data = html_meta_data_parse.get_meta_data_by_url(url)

    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]
    assert "test article" == meta_data["type"]
    assert "@test" == meta_data["twitter_handle"]
    assert "Site Name" == meta_data["site_name"]
    assert "https://www.cnn.com/" == meta_data["url"]

    """ Property Attributes """
    html_dict_arr = [
        {
            "meta": {
                "attributes": {"content": "John Smith", "property": "article:publisher"}
            }
        },
        {
            "meta": {
                "attributes": {
                    "content": "Loves the Water",
                    "property": "og:description",
                }
            }
        },
        {
            "meta": {
                "attributes": {"content": "About John Smith", "property": "og:title"}
            }
        },
        {
            "meta": {
                "attributes": {
                    "content": "https://imageurl.com",
                    "property": "og:image",
                }
            }
        },
        {
            "meta": {
                "attributes": {
                    "content": "https://videourl.com",
                    "property": "og:video",
                }
            }
        },
        {
            "meta": {
                "attributes": {
                    "content": "https://audiourl.com",
                    "property": "og:audio",
                }
            }
        },
        {"meta": {"attributes": {"content": "01/10/2090", "property": "og:pubdate"}}},
        {"meta": {"attributes": {"content": "test article", "property": "og:type"}}},
        {"meta": {"attributes": {"content": "@test", "property": "og:twitter:site"}}},
        {
            "meta": {
                "attributes": {"content": "https://www.cnn.com/", "property": "og:url"}
            }
        },
        {"meta": {"attributes": {"content": "@test", "property": "og:twitter:site"}}},
        {"meta": {"attributes": {"content": "Site Name", "property": "og:site_name"}}},
    ]

    test_html = build_html_fixt(html_dict_arr)

    meta_data = html_meta_data_parse.get_meta_data_by_html(test_html)

    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]
    assert "test article" == meta_data["type"]
    assert "@test" == meta_data["twitter_handle"]
    assert "Site Name" == meta_data["site_name"]
    assert "https://www.cnn.com/" == meta_data["url"]

    """By Url"""
    url = test_links[0]
    requests_mock.get(url, text=test_html)
    meta_data = html_meta_data_parse.get_meta_data_by_url(url)
    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]
    assert "test article" == meta_data["type"]
    assert "@test" == meta_data["twitter_handle"]
    assert "Site Name" == meta_data["site_name"]
    assert "https://www.cnn.com/" == meta_data["url"]

    """ ItemProp Attributes """
    html_dict_arr = [
        {"meta": {"attributes": {"content": "John Smith", "itemprop": "author"}}},
        {
            "meta": {
                "attributes": {"content": "Loves the Water", "itemprop": "description"}
            }
        },
        {"meta": {"attributes": {"content": "About John Smith", "itemprop": "title"}}},
        {
            "meta": {
                "attributes": {"content": "https://imageurl.com", "itemprop": "image"}
            }
        },
        {
            "meta": {
                "attributes": {"content": "https://videourl.com", "itemprop": "video"}
            }
        },
        {
            "meta": {
                "attributes": {"content": "https://audiourl.com", "itemprop": "audio"}
            }
        },
        {"meta": {"attributes": {"content": "01/10/2090", "itemprop": "dateModified"}}},
    ]

    """By Html"""
    meta_data = html_meta_data_parse.get_meta_data_by_html(test_html)

    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]

    """By Url"""
    url = test_links[0]
    requests_mock.get(url, text=test_html)
    meta_data = html_meta_data_parse.get_meta_data_by_url(url)
    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]

    """override meta keys"""
    ov_meta_keys = {
        "testauthor": {"testname": ["test_namr"]},
        "testtitle": {"testproperty": ["test_title"]},
        "testimage": {"testprop": ["test_img"]},
    }

    ov_html_dict_arr = [
        {"meta": {"attributes": {"content": "John Smith", "testname": "test_namr"}}},
        {
            "meta": {
                "attributes": {"content": "Water Title", "testproperty": "test_title"}
            }
        },
        {
            "meta": {
                "attributes": {
                    "content": "https://imageurl.com",
                    "testprop": "test_img",
                }
            }
        },
    ]

    ov_test_html = build_html_fixt(ov_html_dict_arr)

    """By Html"""
    meta_data = html_meta_data_parse.get_meta_data_by_html(
        ov_test_html, override_meta_keys=ov_meta_keys
    )

    assert "John Smith" == meta_data["testauthor"]
    assert "Water Title" == meta_data["testtitle"]
    assert "https://imageurl.com" == meta_data["testimage"]
    assert meta_data["title"] is None
    assert "" == meta_data["content"]

    """By Url"""
    url = test_links[0]
    requests_mock.get(url, text=test_html)
    meta_data = html_meta_data_parse.get_meta_data_by_url(url)
    assert "John Smith" == meta_data["author"]
    assert "About John Smith" == meta_data["title"]
    assert "Loves the Water" == meta_data["content"]
    assert "https://imageurl.com" == meta_data["image"]
    assert "https://videourl.com" == meta_data["media"]
    assert "https://audiourl.com" == meta_data["audio"]
    assert "01/10/2090" == meta_data["pubdate"]


def test_build_html(build_html_fixt):
    html_dict_arr = [
        {"meta": {"attributes": {"content": "John Smith", "name": "author"}}},
        {
            "body": {
                "attributes": {"class": "align"},
                "body": "This is a body",
                "child_arr": [
                    {
                        "div": {
                            "attributes": {"class": "align-div", "id": "divid"},
                            "body": "This is a div",
                        }
                    },
                ],
            }
        },
    ]

    test_html = build_html_fixt(html_dict_arr)
    expected_html = "<html><meta content='John Smith'  name='author' ></meta><body class='align' >This is a body<div class='align-div'  id='divid' >This is a div</div></body></html>"
    assert expected_html == test_html


def test_meta_class_attr():
    html_meta_data_parse = HtmlMetaDataParse()
    assert hasattr(html_meta_data_parse, "proxy")
    assert hasattr(html_meta_data_parse, "override_meta_keys")
    assert hasattr(html_meta_data_parse, "url")
    assert hasattr(html_meta_data_parse, "html_text")
    assert hasattr(html_meta_data_parse, "meta_keys")


def test_other_funcs():
    assert "This is a test" == format_to_fine_content(["<body> This is a test </body>"])
    assert "This is a test " == format_content_list(["This is a test"])
