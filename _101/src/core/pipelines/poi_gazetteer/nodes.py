import os
import subprocess


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