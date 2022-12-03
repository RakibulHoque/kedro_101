from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    extract_zipped_data_to_folder, 
)


def create_pipeline(**kwargs) -> Pipeline:
    bangladesh_pbf_download_pipeline = Pipeline(
        [
            node(
                func=lambda x: getattr(x, "content"),
                inputs="bangladesh_pbf_api",
                outputs="bangladesh_pbf",
                name="url_download.pbf",
            ),
        ]
    )
    gazetteer_jar_download_pipeline = Pipeline(
        [
            node(
                func=lambda x: getattr(x, "content"),
                inputs="gazetteer_download_api",
                outputs="gazetteer_jar",
                name="url_download.gazetteer",
            ),
        ]
    )
    osmconvert_download_pipeline = Pipeline(
        [
            node(
                func=lambda x: getattr(x, "content"),
                inputs="osmconvert_download_api@windows",
                outputs="osmconvert_exe",
                name="url_download.osmconvert_executable",
            ),
        ]
    )
    osmosis_download_pipeline = Pipeline(
        [
            node(
                func=extract_zipped_data_to_folder,
                inputs=[
                    "osmosis_download_api@windows", 
                    "params:osmosis_libpath"
                ],
                outputs="dummy_url_library_extraction.osmosis_libpath.confirmation",
                name="url_download.osmosis_library",
            ),
        ]
    )
    return (
        bangladesh_pbf_download_pipeline 
        + gazetteer_jar_download_pipeline
        + osmconvert_download_pipeline
        + osmosis_download_pipeline
    )
