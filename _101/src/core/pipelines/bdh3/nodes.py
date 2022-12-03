import os

import regex
import numpy as np
import pandas as pd
import h3
import h3pandas # must be imported
from googletrans import Translator
from .utils import md5hash, isEnglish, pdCorrectGibbarish, enbn_from_string, enbn_from_dictionary_parts


GLOBAL_SEPARATOR = ", "


def convert_gadm_level_to_h3(all_geojson_bangladesh, h3_level=9, file_to_read='gadm41_BGD_4.json'):
    bd_level4 = all_geojson_bangladesh[file_to_read]()

    gdf = bd_level4[["geometry"]]
    gdf = gdf.h3.polyfill(int(h3_level))

    bd_level4 = bd_level4[["COUNTRY", "NAME_1", "NAME_2", "NAME_3", "NAME_4"]]
    bd_level4.columns = ["country", "division", "district", "thana", "union"]
    h3_data = gdf[["h3_polyfill"]].join(bd_level4)
    h3_data["region_hash"] = h3_data.apply(lambda x: md5hash("-".join((x["country"], x["division"], x["district"], x["thana"], x["union"]))), axis = 1)
    h3_data.rename(columns={"h3_polyfill": "h3level9"}, inplace=True)
    h3_data = h3_data.explode("h3level9")
    return h3_data
    separator = GLOBAL_SEPARATOR
    enlist = []
    bnlist = []
    name_translate_en2bn = None
    name_translate_bn2en = None
    if not isinstance(addr_dictionary, dict):
        return separator.join(enlist), separator.join(bnlist), name_translate_en2bn, name_translate_bn2en
    for part in addr_dictionary.get("parts"):
        if part and part.get("names", None): 
            name_keys = list(part.get("names").keys())
            for tag, value in part.get("names").items():
                extracted_bn_from_name = []
                extracted_en_from_name = []
                if tag == "name":
                    words = value.split(" ")
                    for word in words:
                        if bool(regex.fullmatch(r'\P{L}*\p{Bengali}+(?:\P{L}+\p{Bengali}+)*\P{L}*', word)):
                            extracted_bn_from_name.append(word)
                        elif bool(regex.fullmatch(r'\P{L}*\p{Bengali}+(?:\P{L}+\p{Bengali}+)*\P{L}*', word.encode("cp1252", "ignore").decode("utf-8", "ignore"))):
                            extracted_bn_from_name.append(word)
                        elif isEnglish(word):
                            extracted_en_from_name.append(word)
                        
                    if extracted_en_from_name: enlist.append(" ".join(extracted_en_from_name))
                    if extracted_bn_from_name: bnlist.append(" ".join(extracted_bn_from_name))
                    if extracted_en_from_name and not extracted_bn_from_name:
                        if part.get("lvl") in ['street'] and "name:bn" not in name_keys:
                            name_translate_en2bn = " ".join(extracted_en_from_name)
                    if not extracted_en_from_name and extracted_bn_from_name:
                        if part.get("lvl") in ['street'] and "name:en" not in name_keys:
                            name_translate_bn2en = " ".join(extracted_bn_from_name)
                if tag == "name:en":
                    enlist.append(value)
                if tag == "name:bn":
                    words = value.split(" ")
                    if words and bool(regex.fullmatch(r'\P{L}*\p{Bengali}+(?:\P{L}+\p{Bengali}+)*\P{L}*', words[0])):
                        bnlist.append(value)
                    else: 
                        bnlist.append(value.encode("cp1252", "ignore").decode("utf-8", "ignore"))
        else:
            return np.nan, np.nan, name_translate_en2bn, name_translate_bn2en
    enlist = list(dict.fromkeys(enlist))    
    bnlist = list(dict.fromkeys(bnlist))
    return separator.join(enlist), separator.join(bnlist), name_translate_en2bn, name_translate_bn2en


def pois_to_h3_mapping(pois, geoh3mapping, h3_level, savedir):
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    counter = 1
    poi_columns = ["osm_id", "h3level9", "lat", "lon", "name", "name_en", "name_bn", 
              "need_translate_en2bn", "need_translate_bn2en",
              "alt_names", "local_admin_name", "admin0_name", "admin2_name", 
              "addr_level", "poi_addr_match", "poi_class", "poi_keywords"]
    
    separator = GLOBAL_SEPARATOR
    for i, poibatch in enumerate(pois):
        print(f"{i} out of 26")
        counter = counter + i
        
        # if i < 26:
        #     continue
        try:
            poibatch["h3level9"] = poibatch["center_point"].apply(lambda x: h3.geo_to_h3(lat=x.get('lat'), lng=x.get('lon'), resolution=h3_level) if isinstance(x, dict) else None)
            poibatch["lat"] = poibatch["center_point"].apply(lambda x: x.get('lat') if isinstance(x, dict) else None)
            poibatch["lon"] = poibatch["center_point"].apply(lambda x: x.get('lon') if isinstance(x, dict) else None)

            poibatch["name"] = poibatch["name"].apply(pdCorrectGibbarish)
            if "alt_names" in poibatch.columns:
                poibatch["alt_names"] = poibatch["alt_names"].apply(pdCorrectGibbarish)
            if "local_admin_name" in poibatch.columns:
                poibatch["local_admin_name"] = poibatch["local_admin_name"].apply(pdCorrectGibbarish)
            poibatch["admin0_name"] = poibatch["admin0_name"].apply(pdCorrectGibbarish)
            poibatch["admin2_name"] = poibatch["admin2_name"].apply(pdCorrectGibbarish)
            poibatch["addr_level"] = poibatch["addr_level"].apply(pdCorrectGibbarish)
            if "poi_addr_match" in poibatch.columns:
                poibatch["poi_addr_match"] = poibatch["poi_addr_match"].apply(pdCorrectGibbarish)
            if "poi_class" in poibatch.columns:    
                poibatch["poi_class"] = poibatch["poi_class"].apply(pdCorrectGibbarish)
            if "poi_keywords" in poibatch.columns: 
                poibatch["poi_keywords"] = poibatch["poi_keywords"].apply(pdCorrectGibbarish)

            poibatch["name_en_short"], poibatch["name_bn_short"], poibatch["need_translate_en2bn_short"], poibatch["need_translate_bn2en_short"] \
                    = zip(*poibatch["name"].apply(lambda x: enbn_from_string(x)))
            poibatch["name_en_extension"], poibatch["name_bn_extension"], poibatch["need_translate_en2bn_extension"], poibatch["need_translate_bn2en_extension"] \
                = zip(*poibatch["address"].apply(lambda x: enbn_from_dictionary_parts(x)))

            poibatch["name_en"] = (poibatch["name_en_short"].fillna("") + separator + poibatch["name_en_extension"].fillna("")).str.lstrip(separator).fillna('')
            poibatch["name_bn"] = (poibatch["name_bn_short"].fillna("") + separator + poibatch["name_bn_extension"].fillna("")).str.lstrip(separator).fillna('')
            poibatch["name_en"] = poibatch["name_en"].str.split(separator).apply(lambda x: separator.join(list(dict.fromkeys(x))))
            poibatch["name_bn"] = poibatch["name_bn"].str.split(separator).apply(lambda x: separator.join(list(dict.fromkeys(x))))

            poibatch["need_translate_en2bn"] = (poibatch["need_translate_en2bn_short"].fillna("") + separator + poibatch["need_translate_en2bn_extension"].fillna("")).str.lstrip(separator).fillna('')
            poibatch["need_translate_bn2en"] = (poibatch["need_translate_bn2en_short"].fillna("") + separator + poibatch["need_translate_bn2en_extension"].fillna("")).str.lstrip(separator).fillna('')
            poibatch["need_translate_en2bn"] = poibatch["need_translate_en2bn"].str.split(separator).apply(lambda x: separator.join(list(dict.fromkeys(x))))
            poibatch["need_translate_bn2en"] = poibatch["need_translate_bn2en"].str.split(separator).apply(lambda x: separator.join(list(dict.fromkeys(x))))
            
            poibatch["name_en"] = poibatch["name_en"].apply(pdCorrectGibbarish)
            poibatch["name_bn"] = poibatch["name_bn"].apply(pdCorrectGibbarish)
            poibatch["need_translate_en2bn"] = poibatch["need_translate_en2bn"].apply(pdCorrectGibbarish)
            poibatch["need_translate_bn2en"] = poibatch["need_translate_bn2en"].apply(pdCorrectGibbarish)

            found_columns = set(poibatch.columns)
            missing_columns = set(poi_columns).union(found_columns) - found_columns
            if missing_columns:
                for col in missing_columns:
                    poibatch[col] = np.nan

            poibatch = poibatch[poi_columns]
            batch_result = poibatch.merge(geoh3mapping, how="left", on="h3level9")
            batch_result["district"] = batch_result["district"].fillna('foo')
            batch_groups = batch_result.groupby(by="district")
            for gk, grp in batch_groups:
                gk_filepath = os.path.join(savedir, f"{gk}.csv").replace("\\", "/")
                if not os.path.exists(gk_filepath):
                    grp.to_csv(gk_filepath)
                else:
                    grp.to_csv(gk_filepath, mode='a', header=False)
        except Exception as e:
            print(f"Exception occurred at i={i}: {e}")
            continue

    return dict(status=True)


def get_translation_from_archive_words(district_poi_dict, archive_en2bn, archive_bn2en, *args):
    # for key, value in district_poi_dict.items():
    #     district_poi_data = value()
    pass
        


def get_translation_required_words(district_poi_dict, *args):
    en_set = set()
    bn_set = set()
    for key, value in district_poi_dict.items():
        district_poi_data = value()
        en_set = en_set.union(set(district_poi_data[~district_poi_data["need_translate_en2bn"].isna()]["need_translate_en2bn"].unique().tolist()))
        bn_set = bn_set.union(set(district_poi_data[~district_poi_data["need_translate_bn2en"].isna()]["need_translate_bn2en"].unique().tolist()))
    return pd.DataFrame(data=list(en_set), columns=["en_phrases"]), pd.DataFrame(data=list(bn_set), columns=["bn_phrases"])



def run_infinitely(data: pd.DataFrame, tmp_save_path="infinite.csv", source_lan=None, translated_to=None):
    if not os.path.exists(path:=os.path.dirname(tmp_save_path)):
        os.makedirs(path)
    data_len = len(data[f"{source_lan}_phrases"])
    translator = Translator()
    base_collected_data = []
    translated_data = None
    counter = 0
    while True:
        if counter >= data_len - 1:
            break
        translated_words = {}
        try:
            for i, word_to_translate in enumerate(data[f"{source_lan}_phrases"]):
                if i <= counter:
                    continue
                translated_words[word_to_translate] = translator.translate(word_to_translate, src=source_lan, dest=translated_to)
                print(f"completed {i} out of {data_len}, more time required: {(data_len-i)/1800:.2f} hrs")
        except KeyboardInterrupt:
            for word_to_translate, translated_obj in translated_words.items():
                base_collected_data.append((word_to_translate, translated_obj.text))
                translated_data = pd.DataFrame(data=base_collected_data, columns=[f"{source_lan}_phrases", f"{translated_to}_translated"])
            translated_data.to_csv(tmp_save_path)
            break
        except Exception as e:
            for word_to_translate, translated_obj in translated_words.items():
                base_collected_data.append((word_to_translate, translated_obj.text))
                translated_data = pd.DataFrame(data=base_collected_data, columns=[f"{source_lan}_phrases", f"{translated_to}_translated"])
            translated_data.to_csv(tmp_save_path)
        else:
            for word_to_translate, translated_obj in translated_words.items():
                base_collected_data.append((word_to_translate, translated_obj.text))
                translated_data = pd.DataFrame(data=base_collected_data, columns=[f"{source_lan}_phrases", f"{translated_to}_translated"])
        finally:
            counter = i
    translated_data.to_csv(tmp_save_path) 
    return translated_data

