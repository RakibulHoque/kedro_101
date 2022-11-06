from kedro.pipeline import Pipeline, node, pipeline
from .nodes import convert_gadm_level_to_h3, pois_to_h3_mapping


def create_pipeline(**kwargs) -> Pipeline:
    h3_data_extraction_pipeline = Pipeline(
        [
            node(
                func=convert_gadm_level_to_h3,
                inputs=[
                    "geojson_bangladesh@gpd",
                    "params:h3_level_for_joining"
                ],
                outputs="geojson_bangladesh_h3_level9",
                name="conversion.geojson_to_h3",
            )
        ]
    )
    poi_h3_data_mapping_pipeline = Pipeline(
        [
            node(
                func=pois_to_h3_mapping,
                inputs=[
                    "bangladesh_pois_json@local",
                    "geojson_bangladesh_h3_level9",
                    "params:h3_level_for_joining",
                    "params:district_level_poi_savedir"
                ],
                outputs="dummy_execute_h3mapping.district_poi.confirmation",
                name="conversion.poi_to_h3",
            )
        ]
    )
    return h3_data_extraction_pipeline + poi_h3_data_mapping_pipeline
    # return  poi_h3_data_mapping_pipeline

