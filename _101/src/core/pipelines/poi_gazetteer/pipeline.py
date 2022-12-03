from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    execute_osmconvert_pbf_to_osm,
    execute_gazetteer_split_command,
    execute_gazetteer_slice_command,
    execute_gazetteer_join_command
)


def create_pipeline(**kwargs) -> Pipeline:
    poi_gazetteer_filter_pipeline = Pipeline(
        [
            node(
                func=execute_osmconvert_pbf_to_osm,
                inputs=[
                    "osmconvert_exe", 
                    "bangladesh_pbf",
                    "params:bangladesh_osm_filename",
                    "gazetteer_jar"
                ],
                outputs="dummy_execute_osmconvert.bangladesh_osm.confirmation",
                name="execute_osmconvert.bangladesh_osm",
            ),
            node(
                func=execute_gazetteer_split_command,
                inputs=[
                    "gazetteer_jar",
                    "bangladesh_osm",
                    "params:gazetteer_data_storage_path",
                    "dummy_execute_osmconvert.bangladesh_osm.confirmation"
                ],
                outputs="dummy_execute_gazetteer.split.confirmation",
                name="execute_gazetteer.split",
            ),
            node(
                func=execute_gazetteer_slice_command,
                inputs=[
                    "gazetteer_jar",
                    "params:gazetteer_data_storage_path",
                    "dummy_execute_gazetteer.split.confirmation"
                ],
                outputs="dummy_execute_gazetteer.slice.confirmation",
                name="execute_gazetteer.slice",
            ),
            node(
                func=execute_gazetteer_join_command,
                inputs=[
                    "gazetteer_jar",
                    "params:gazetteer_data_storage_path",
                    "params:gazetteer_json_zip_filepath",
                    "dummy_execute_gazetteer.slice.confirmation"
                ],
                outputs="dummy_execute_gazetteer.bangladesh_pois_json_zip.confirmation",
                name="execute_gazetteer.join",
            )
        ]
    )
    return poi_gazetteer_filter_pipeline

