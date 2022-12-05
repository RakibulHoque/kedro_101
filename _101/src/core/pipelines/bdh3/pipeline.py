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
    # Spans the whole bangladesh using h3
    h3_spanning_pipeline = Pipeline(
        [
            node(
                func=convert_gadm_level_to_h3,
                inputs=[
                    "gadm_bangladesh@gpd",
                    "params:h3_level_for_joining"
                ],
                outputs="geojson_bangladesh_h3_level9",
                name="conversion.geojson_to_h3",
            )
        ]
    )
    # Joins with POI h3 to get the zone names
    h3_joining_pipeline = Pipeline(
        [
            node(
                func=pois_to_h3_mapping,
                inputs=[
                    "gazetteer_pois_json@local",
                    "geojson_bangladesh_h3_level9",
                    "params:h3_level_for_joining",
                    "params:district_level_poi_savedir"
                ],
                outputs="dummy_execute_h3mapping.district_poi.confirmation",
                name="conversion.poi_to_h3",
            ),
        ]
    )
    # Translates bangla to english, english to bangla
    translation_pipeline = Pipeline(
        [
            node(
                func=get_translation_required_words,
                inputs=[
                    "district_poi",
                    # "dummy_execute_h3mapping.district_poi.confirmation"
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
    archived_translation_pipeline = Pipeline(
        [ 
            node(
                func=get_translation_from_archive_words,
                inputs=[
                    "district_poi",
                    "archive_en2bn_translated",
                    "archive_bn2en_translated",
                    # "dummy_execute_h3mapping.district_poi.confirmation"
                ],
                outputs="district_poi_with_modified_names",
                name="collection.required_translation_replace",
            ),
        ]
    )
    return (
        # h3_spanning_pipeline 
        # + h3_joining_pipeline 
        # + translation_pipeline
        archived_translation_pipeline
    )
