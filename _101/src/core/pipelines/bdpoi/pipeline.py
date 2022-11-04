from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    execute_osmconvert_all_elements_to_nodes, 
    extract_zipped_data_to_folder, 
    execute_osmosis_node_to_poi,
    execute_osmconvert_poi_to_csv
)


def create_pipeline(**kwargs) -> Pipeline:
    poi_osmconvert_extraction_pipeline = Pipeline(
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
            ),
            node(
                func=execute_osmconvert_all_elements_to_nodes,
                inputs=["osmconvert_exe", "bangladesh_pbf"],
                outputs="dummy_execute_osmconvert.element_to_node.confirmation",
                name="execute_osmconvert.element_to_node_conversion",
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
                outputs="dummy_url_library_extraction.osmosis.confirmation",
                name="url_download.osmosis_library",
            ),
            node(
                func=execute_osmosis_node_to_poi,
                inputs=[
                    "params:osmosis_libpath", 
                    "bangladesh_pbf_allnodes", 
                    "dummy_url_library_extraction.osmosis.confirmation", 
                    "dummy_execute_osmconvert.element_to_node.confirmation"
                ],
                outputs="dummy_execute_osmosis.node_filtering.confirmation",
                name="execute_osmosis.node_filter",
            ),
            node(
                func=execute_osmconvert_poi_to_csv,
                inputs=[
                    "osmconvert_exe", 
                    "bangladesh_pbf_allpois", 
                    # "dummy_execute_osmosis.node_filtering.confirmation"
                ],
                outputs="dummy_execute_osmconvert.filtered_nodes_to_csv.confirmation",
                name="execute_osmconvert.csv_conversion",
            ),
        ]
    )
    return poi_osmconvert_extraction_pipeline + poi_osmosis_filter_pipeline

