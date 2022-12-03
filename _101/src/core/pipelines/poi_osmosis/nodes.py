import os
import subprocess


def execute_osmconvert_all_elements_to_nodes(osmconvert_exe, bangladesh_pbf, bangladesh_pbf_allnodes_filename):
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf), bangladesh_pbf_allnodes_filename).replace("\\", "/")
    cmd = f"{osmconvert_exe} --all-to-nodes --max-objects=500000000 {bangladesh_pbf} -o={output_savepath}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def execute_osmosis_node_to_poi(osmosis_libpath, bangladesh_pbf_allnodes, bangladesh_pbf_allpois_filename,*args):    

    osmosis_exe = os.getcwd().replace("\\", "/") + "/" + osmosis_libpath + "/bin/osmosis.bat"
    bangladesh_pbf_allnodes_filepath = bangladesh_pbf_allnodes.replace("\\", "/")
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf_allnodes), bangladesh_pbf_allpois_filename).replace("\\", "/")

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


def execute_osmconvert_poi_to_csv(osmconvert_exe, bangladesh_pbf_allpois, bangladesh_pois_csv_filename, *args):
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf_allpois), "../csv", bangladesh_pois_csv_filename).replace("\\", "/")
    if not os.path.exists(os.path.dirname(output_savepath)):
        os.makedirs(os.path.dirname(output_savepath))
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


def execute_osmconvert_pbf_to_osm(osmconvert_exe, bangladesh_pbf, bangladesh_osm_filename, *args):
    output_savepath = os.path.join(os.path.dirname(bangladesh_pbf), "../json", bangladesh_osm_filename).replace("\\", "/")
    cmd = f"{osmconvert_exe} {bangladesh_pbf} -o={output_savepath}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def execute_gazetteer_split_command(gazetteer_jar, bangladesh_osm, gazetteer_data_storage_path, *args):
    cmd = f"java -jar {gazetteer_jar} --data-dir {gazetteer_data_storage_path} split {bangladesh_osm}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def execute_gazetteer_slice_command(gazetteer_jar, gazetteer_data_storage_path, *args):
    cmd = f"java -jar {gazetteer_jar} --data-dir {gazetteer_data_storage_path} slice"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def execute_gazetteer_join_command(gazetteer_jar, gazetteer_data_storage_path, gazetteer_json_zip_filepath, *args):
    cmd = f"java -jar {gazetteer_jar} --data-dir {gazetteer_data_storage_path} join --handlers out-gazetteer {gazetteer_json_zip_filepath}"
    print(cmd)
    subprocess.run(cmd)
    return dict(status=True)


def foo_command(*args):
    return dict(status=True)