import json
from urllib import request
from xml.etree import ElementTree as Et


def strip_text(xml_array, tag, text_type, default):
    """
    Parses XML attributes along the same level
    :param xml_array: XML attributes (list)
    :param tag: name of XML tag to search for (str)
    :param text_type: what type the field contents are expected to be (data type)
    :param default: default value if tag field is empty or does not match data type
    :return: str if text_type is str, else list
    """

    data = [item.text if isinstance(item.text, text_type) else default for item in xml_array if xml_array.tag == tag]
    if text_type == str:
        return ". ".join(data)
    return data


def process_xml(xml_string):
    """
    Processes XML from a string literal
    :param xml_string: (str)
    :return: desired attributes in JSON form (dict)
    """

    root = Et.fromstring(xml_string)

    docs = {}
    for child in root:
        # get ID, text pair out of XML
        pair = [field.text if field.tag == 'iati-identifier' else strip_text(field, 'description', str, "")
                for field in child if field.tag in {'iati-identifier', 'description'}]
        idx, text = pair
        temp_dict = {idx: {"text": text}}
        docs = {**docs, **temp_dict}

    return docs


def classify(data):
    """
    Sample batch request to the auto-classification API
    :param data: (dict)
    :return: (JSON)
    """
    
    url = "http://hostname:9091/batch"
    opts = {"data": data,
            "chunk": "true",
            "threshold": "low",
            "rollup": "false"
            }

    req = request.Request(url, data=json.dumps(opts).encode('utf8'), headers={"Content-Type": "application/json"})
    return request.urlopen(req).read().decode('utf8')


if __name__ == '__main__':
    with open('iati_sample_1.xml', 'r') as f:
        d = f.read()

    parsed_data = process_xml(d)
    p = classify(data=parsed_data)
    print(p)
