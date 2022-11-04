import os
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path


def execute_osmconvert_all_elements_to_nodes(osmconvert_exe, bangladesh_pbf):
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf), "bangladesh-latest-allnodes.osm.pbf").replace("\\", "/")
    cmd = f"{osmconvert_exe} --all-to-nodes --max-objects=500000000 {bangladesh_pbf} -o={output_savepath}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def extract_zipped_data_to_folder(response, osmosis_path):
    z = zipfile.ZipFile(BytesIO(response.content))
    z.extractall(osmosis_path)
    return {"status": True}


def execute_osmosis_node_to_poi(osmosis_libpath, bangladesh_pbf_allnodes, *args):    

    osmosis_exe = os.getcwd().replace("\\", "/") + "/" + osmosis_libpath + "/bin/osmosis.bat"
    bangladesh_pbf_allnodes_filepath = bangladesh_pbf_allnodes.replace("\\", "/")
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf_allnodes), "poinode.osm.pbf").replace("\\", "/")

    filter_command = " ".join((
        f"--rbf",
        f"{bangladesh_pbf_allnodes_filepath}",
        f"--tf accept-nodes",
        f"addr:housenumber=* addr:housename=* addr:flat=* addr:flats=* addr:unit=*",
        f"addr:conscriptionnumber=* addr:streetnumber=* addr:street=* addr:place=* addr:postbox=* addr:postcode=* addr:city=* addr=*",
        f"addr:full=* addr:town=* addr:quarter=* addr:suburb=* addr:subdistrict=* addr:district=* addr:province=* addr:region=*",
        f"addr:state=* addr:county=* addr:country=* amenity=* source:name=* name=* name:en=* name:bn=* name:left=* name:right=*",
        f"int_name=* int_name:en=* int_name:bn=* loc_name=* loc_name:en=* loc_name:bn=* nat_name=* nat_name:en=* nat_name:bn=*",
        f"official_name=* official_name:en=* official_name:bn=* old_name=* reg_name=* reg_name:en=* reg_name:bn=* short_name=*",
        f"short_name:en=* short_name:bn=* sorting_name=* alt_name=* --tf reject-ways --tf reject-relations",
        f"--wx {output_savepath}"
    ))

    cmd = f"{osmosis_exe} {filter_command}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def execute_osmconvert_poi_to_csv(osmconvert_exe, bangladesh_pbf_allpois, *args):
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf_allpois), "poinode.csv").replace("\\", "/")
    cmd = " ".join((
        f'{osmconvert_exe} {bangladesh_pbf_allpois}',
        f'-o={output_savepath}',
        f'--csv="@id @lon @lat name addr:city addr:postcode addr:district',
        f'amenity place addr:street addr:country addr:housenumber building:material',
        f'name:en addr:union addr:ward addr:province addr:division addr:subdistrict',
        f'addr:state name:bn addr:suburb addr:word addr:neighbourhood addr:place alt_name addr:housename"',
        f'--csv-headline --csv-separator=,'
        ))
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)