

def build_html(
    html_dict_arr,
    child_dict_arr=False
):
    html_body = ""
    if not child_dict_arr:
        html_body = "<html>"
    for html_dict in html_dict_arr:
        for type, type_content in html_dict.items():
            html_body += "<{}".format(type)
            attributes_c = ">"
            attributes = type_content.get("attributes", {})
            body = type_content.get("body")
            attr_build = ""
            for k, v in attributes.items():
                attr_build += " {}='{}' ".format(k, v)
            if body:
                html_body += "{}{}{}".format(
                    attr_build,
                    attributes_c,
                    body,
                )
            else:
                html_body += "{}{}".format(
                    attr_build,
                    attributes_c
                )
            child_arr = type_content.get("child_arr")
            if child_arr:
                html_body += "{}".format(
                    build_html(child_arr, child_dict_arr=True)
                )

            html_body += "</{}>".format(type)
    if not child_dict_arr:
        html_body += "</html>".format(type)

    return html_body
