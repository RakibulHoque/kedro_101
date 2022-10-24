import re


import zipfile
from io import BytesIO

def extract_zipped_data(*args):
    datamap = {}
    for r in args:
        z = zipfile.ZipFile(BytesIO(r.content))
        filename = z.infolist()[0].filename
        unzipped_content = z.read(filename).decode("utf-8")
        datamap[filename] = unzipped_content
    return datamap