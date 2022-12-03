from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    execute_osmconvert_all_elements_to_nodes, 
    execute_osmosis_node_to_poi,
    execute_osmconvert_poi_to_csv,
)


def create_pipeline(**kwargs) -> Pipeline:
    poi_osmosis_filter_pipeline = Pipeline(
        [   
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
    return poi_osmosis_filter_pipeline

