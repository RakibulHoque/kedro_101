import re
import regex
import hashlib
import numpy as np


#utils
def md5hash(s: str): 
    return hashlib.md5(s.encode('utf-8')).hexdigest()


#utils
# -*- coding: utf-8 -*-
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

#utils
def isBengali(s):
    return bool(regex.fullmatch(r'\P{L}*\p{Bengali}+(?:\P{L}+\p{Bengali}+)*\P{L}*', s))

#utils
def splitter(s, seps=[";", ",", " ", "\*", "\(", "\)"]):
    regex_expression = "|".join(seps)
    parts = re.split(regex_expression, s)
    return [part for part in parts if part]

#utils
def isGibbarish(s):
    for word in splitter(s):
        if not(isEnglish(word) or isBengali(word)):
            return True
    return False

#utils
def correctGibbarish(s, encoder="cp1252"):
    return s.encode(encoder, "ignore").decode("utf-8", "ignore")


#utils
def enbn_from_string(s: str, conn_sep = " "):
    en2bn, bn2en = None, None
    enlist, bnlist = [], []

    if isinstance(s, str):
        if isGibbarish(s):
            s = correctGibbarish(s)

        all_words = splitter(s)

        if isBengali(s):
            bn2en = conn_sep.join(all_words)
        elif isEnglish(s):
            en2bn = conn_sep.join(all_words) 
        
        for word in all_words:
            if isBengali(word):
                bnlist.append(word)
            elif isEnglish(word):
                enlist.append(word)
            
    return conn_sep.join(enlist), conn_sep.join(bnlist), en2bn, bn2en

#utils
def enbn_from_dictionary_parts(addr_dictionary, separator = ", "): 
    
    enlist , bnlist = [], []
    name_translate_en2bn, name_translate_bn2en = None, None
    
    if not isinstance(addr_dictionary, dict):
        return separator.join(enlist), separator.join(bnlist), name_translate_en2bn, name_translate_bn2en

    for part in addr_dictionary.get("parts"):
        if part and part.get("names", None): 
            name_keys = list(part.get("names").keys())
            for tag, value in part.get("names").items():
                extracted_bn_from_name, extracted_en_from_name = [], []
                if tag == "name":
                    all_words = splitter(value)
                    for word in all_words:
                        if isBengali(word):
                            extracted_bn_from_name.append(word)
                        elif isGibbarish(word):
                            extracted_bn_from_name.append(correctGibbarish(word))
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
                    if isEnglish(value):
                        enlist.append(value)
                if tag == "name:bn":
                    if isGibbarish(value):
                        bnlist.append(correctGibbarish(value))
                    else: 
                        bnlist.append(value)
        else:
            return np.nan, np.nan, name_translate_en2bn, name_translate_bn2en
    enlist = list(dict.fromkeys(enlist))    
    bnlist = list(dict.fromkeys(bnlist))
    return separator.join(enlist), separator.join(bnlist), name_translate_en2bn, name_translate_bn2en


def pdCorrectGibbarish(x):
    return correctGibbarish(x) if isinstance(x,str) and isGibbarish(x) else x