from kedro.pipeline import Pipeline, node, pipeline
from .nodes import extract_zipped_data


def create_pipeline(**kwargs) -> Pipeline:
    raw_data_extraction_pipeline = Pipeline(
        [
            node(
                func=extract_zipped_data,
                inputs=[
                    "gadm_bangladesh_level_00_api", 
                    "gadm_bangladesh_level_01_api", 
                    "gadm_bangladesh_level_02_api",
                    "gadm_bangladesh_level_03_api",
                    "gadm_bangladesh_level_04_api",
                ],
                outputs="gadm_bangladesh",
                name="url_data_extraction",
            )
        ]
    )
    return raw_data_extraction_pipeline
