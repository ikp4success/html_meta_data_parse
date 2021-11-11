import requests
from requests import Response
from copy import deepcopy

from parsel import Selector

from html_meta_data_parse.util import (
    format_to_fine_content,
    get_meta_data_keys
)


class HtmlMetaDataParse(object):
    """Parse Meta Data From Web Pages"""
    url = None
    override_meta_keys = None
    html_text = None
    proxy = None
    meta_keys = get_meta_data_keys()

    def __init__(
        self,
        url=None,
        override_meta_keys=None,
        html_text=None,
        proxy=None
    ):
        self.url = url
        self.override_meta_keys = override_meta_keys
        self.html_text = html_text
        self.proxy = proxy

    def get_meta_data_by_url(
        self,
        url=None,
        override_meta_keys=None,
        http_method="HEAD",
        headers=None,
        proxy=None,
    ):
        if http_method not in ["HEAD", "GET"]:
            raise Exception(f"http_method {http_method} is invalid. Allowed Method HEAD, GET.")
        url = url or self.url
        override_meta_keys = override_meta_keys or self.override_meta_keys
        proxy = proxy or self.proxy
        headers = headers or {}
        if url:
            try:
                response = getattr(requests, http_method.lower())(
                    url,
                    headers=headers,
                    proxies=proxy,
                )
                return self.get_meta_data_by_html(
                    html_text=response,
                    override_meta_keys=override_meta_keys
                )
            except Exception as e:
                return {"Error": repr(e)}
        raise Exception("URL is required")

    def get_meta_data_by_html(
        self,
        html_text=None,
        override_meta_keys=None
    ):
        html_text = html_text or self.html_text
        if not html_text:
            raise Exception("html_text is required.")
        try:
            override_meta_keys = override_meta_keys or self.override_meta_keys

            if not html_text:
                return {}

            response = Selector(text=html_text)

            head_title = response.css("head title ::text").extract_first()
            body_content = format_to_fine_content(
                response.css("body")
            )

            meta_css = response.css("meta")
            meta_css_query = "[{}='{}'] ::attr(content)"
            meta_data = {}

            w_meta_keys = deepcopy(self.meta_keys)
            if override_meta_keys:
                w_meta_keys = deepcopy(override_meta_keys)

            for meta_key, meta_value in w_meta_keys.items():
                for meta_value_attr_k, meta_value_attr_v in meta_value.items():
                    for attr in meta_value_attr_v:
                        fr_meta_css_query = meta_css_query.format(
                            meta_value_attr_k,
                            attr
                        )
                        data = meta_css.css(fr_meta_css_query).extract_first()
                        if data:
                            meta_data[meta_key] = data
                            break

            meta_data["title"] = (
                meta_data.get("title") or
                head_title or
            )
            meta_data["content"] = (
                meta_data.get("content") or
                body_content
            )
            return meta_data
        except Exception as e:
            return {
                "Error": repr(e)
            }
