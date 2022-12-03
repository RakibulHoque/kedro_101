import zipfile
from io import BytesIO
from pathlib import Path


def extract_zipped_data_to_folder(response, osmosis_path):
    z = zipfile.ZipFile(BytesIO(response.content))
    z.extractall(osmosis_path)
    return {"status": True}