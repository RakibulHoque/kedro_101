import json
import zipfile
from io import BytesIO


def extract_zipped_data_to_file(*args):
    """
    This function takes url responses from a list of args; extract and save them
    """
    datamap = {}
    for r in args:
        z = zipfile.ZipFile(BytesIO(r.content))
        filename = z.infolist()[0].filename
        unzipped_content = z.read(filename).decode("utf-8")
        datamap[filename] = unzipped_content
    return datamap, {"status": True}


def newline_delimiter_json_builder(geojson_dict, *args):
    """
    This function plain geojson to newline delimited geojsons
    """
    nl_geojson_dict = {}
    for key, exec_func in geojson_dict.items():
        features = exec_func()['features']
        schema = None
        file_content = ''
        for obj in features:
            props = obj['properties'] # a dictionary
            props['geometry'] = json.dumps(obj['geometry']) # make the geometry a string
            file_content = file_content + json.dumps(props) + "\n"
        nl_geojson_dict["nl_" + key] = file_content
    return nl_geojson_dict
