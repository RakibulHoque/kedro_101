from kedro.pipeline import Pipeline, node, pipeline
from .nodes import extract_zipped_data_to_file, newline_delimiter_json_builder


def create_pipeline(**kwargs) -> Pipeline:
    raw_data_extraction_pipeline = Pipeline(
        [
            node(
                func=extract_zipped_data_to_file,
                inputs=[
                    "gadm_bangladesh_level_00_api", 
                    "gadm_bangladesh_level_01_api", 
                    "gadm_bangladesh_level_02_api",
                    "gadm_bangladesh_level_03_api",
                    "gadm_bangladesh_level_04_api",
                ],
                outputs=["gadm_bangladesh", "dummy_url_data_extraction.gadm.confirmation"],
                name="url_data_extraction.gadm",
            ),
            node(
                func=newline_delimiter_json_builder,
                inputs=[
                    "geojson_bangladesh",
                    "dummy_url_data_extraction.gadm.confirmation"
                ],
                outputs="gadm_nl_bangladesh",
                name="nl_json_extraction.gadm",
            ),
            
        ]
    )
    return raw_data_extraction_pipeline
