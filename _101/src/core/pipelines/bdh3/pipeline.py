from functools import partial 
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    convert_gadm_level_to_h3, 
    pois_to_h3_mapping, 
    get_translation_from_archive_words,
    get_translation_required_words, 
    run_infinitely
)


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
            ),
            node(
                func=get_translation_from_archive_words,
                inputs=[
                    "district_poi",
                    "archive_en2bn_translated",
                    "archive_bn2en_translated",
                    "dummy_execute_h3mapping.district_poi.confirmation"
                ],
                outputs=["en_phrases", "bn_phrases"],
                name="collection.required_translation",
            ),
            node(
                func=get_translation_required_words,
                inputs=[
                    "district_poi",
                    "dummy_execute_h3mapping.district_poi.confirmation"
                ],
                outputs=["en_phrases", "bn_phrases"],
                name="collection.required_translation",
            ),
            node(
                func=partial(run_infinitely, source_lan="en", translated_to="bn"),
                inputs=[
                    "en_phrases",
                    "params:tmp_translation_en2bn_saving_filepath"
                ],
                outputs="translated_en2bn_data",
                name="translation.en2bn",
            ),
            node(
                func=partial(run_infinitely, source_lan="bn", translated_to="en"),
                inputs=[
                    "bn_phrases",
                    "params:tmp_translation_bn2en_saving_filepath"
                ],
                outputs="translated_bn2en_data",
                name="translation.bn2en",
            )
        ]
    )
    # return h3_data_extraction_pipeline
    # return  poi_h3_data_mapping_pipeline
    return h3_data_extraction_pipeline + poi_h3_data_mapping_pipeline


