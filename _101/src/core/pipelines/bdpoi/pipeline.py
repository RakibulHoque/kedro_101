from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    execute_osmconvert_all_elements_to_nodes, 
    extract_zipped_data_to_folder, 
    execute_osmosis_node_to_poi,
    execute_osmconvert_poi_to_csv,
    execute_osmconvert_pbf_to_osm,
    execute_gazetteer_split_command,
    execute_gazetteer_slice_command,
    execute_gazetteer_join_command
)


def create_pipeline(**kwargs) -> Pipeline:
    poi_osmconvert_download_pipeline = Pipeline(
        [
            node(
                func=lambda x: getattr(x, "content"),
                inputs="bangladesh_pbf_api",
                outputs="bangladesh_pbf",
                name="url_download.pbf",
            ),
            node(
                func=lambda x: getattr(x, "content"),
                inputs="osmconvert_download_api@windows",
                outputs="osmconvert_exe",
                name="url_download.osmconvert_executable",
            )
        ]
    )
    poi_osmosis_filter_pipeline = Pipeline(
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
            node(
                func=execute_osmconvert_all_elements_to_nodes,
                inputs=[
                    "osmconvert_exe", 
                    "bangladesh_pbf",
                    "params:bangladesh_pbf_allnodes_filename"
                ],
                outputs="dummy_execute_osmconvert.bangladesh_pbf_allnodes.confirmation",
                name="execute_osmconvert.element_to_node_conversion",
            ),
            node(
                func=execute_osmosis_node_to_poi,
                inputs=[
                    "params:osmosis_libpath", 
                    "bangladesh_pbf_allnodes",
                    "params:bangladesh_pbf_allpois_filename",
                    "dummy_url_library_extraction.osmosis_libpath.confirmation", 
                    "dummy_execute_osmconvert.bangladesh_pbf_allnodes.confirmation"
                ],
                outputs="dummy_execute_osmosis.bangladesh_pbf_allpois.confirmation",
                name="execute_osmosis.node_filter",
            ),
            node(
                func=execute_osmconvert_poi_to_csv,
                inputs=[
                    "osmconvert_exe", 
                    "bangladesh_pbf_allpois", 
                    "params:bangladesh_pois_csv_filename",
                    "dummy_execute_osmosis.bangladesh_pbf_allpois.confirmation"
                ],
                outputs="dummy_execute_osmconvert.bangladesh_pois_csv.confirmation",
                name="execute_osmconvert.csv_conversion",
            ),
            node(
                func=lambda x, _: x,
                inputs=["bangladesh_pois_csv@local", "dummy_execute_osmconvert.bangladesh_pois_csv.confirmation"],
                outputs="bangladesh_pois_csv@cloud",
                name="upload_to_cloud.bangladesh_pois_csv",
            ),
        ]
    )
    poi_gazetteer_filter_pipeline = Pipeline(
        [
            node(
                func=lambda x: getattr(x, "content"),
                inputs="gazetteer_download_api",
                outputs="gazetteer_jar",
                name="url_download.gazetteer",
            ),
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
    # return poi_osmconvert_download_pipeline
    # return poi_osmosis_filter_pipeline
    # return poi_gazetteer_filter_pipeline
    # return poi_osmconvert_download_pipeline + poi_osmosis_filter_pipeline
    return poi_osmconvert_download_pipeline + poi_gazetteer_filter_pipeline

