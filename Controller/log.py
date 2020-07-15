"""
log.py contains tools to read and write from the log
"""

# ---------- IMPORTS ----------
import os
import sys
import json
# import psutil
# psutil can be used to indicate the amount of used and remaining
# virtual memory for addressing


# ---------- CUSTOM IMPORTS --------
import pin_constants


# ---------- LOG CONSTANTS ------


MAX_SIZE = 2 ** 30


# ---------- UTILITIES ----------


def append_dict(file_path, new_dict):
    """
    append_dict(file_path, new_dict) appends ne_djct onto the jsopn
    dict at file_path

    REQUIRES: file_path contains a dicitonary that is in JSon format
    REQUIRES: new_dict is a dictionary in JSoN format
    """
    fp = open(file_path, "r")
    old_dict = json.load(fp)
    fp.close()

    for key in new_dict:
        old_dict[key] = new_dict[key]

    fp = open(file_path, "w")
    json.dump(old_dict, fp)
    fp.close()


def merge_dict(file_path, new_dict):
    """
    merge_dict(file_path, new_dict) merges the dictionary file_path with
    the dictionary new_dict togeterher. Removes duplicate keys
    and takes on most recent key in the merge

    REQUIRES: file_path contains a dicitonary that is in JSon format
    REQUIRES: new_dict is a dictionary in JSoN format
    WARNING: REMOVES DUPLICATES
    TOO SLOW FOR LARGE FILES!!!!
    """
    fp = open(file_path, "r")
    old_dict = json.load(fp)
    fp.close()

    for key in new_dict:
        old_dict[key] = new_dict[key]

    fp = open(file_path, "w")
    json.dump(old_dict, fp)
    fp.close()


def get_file_size(file_path):
    """
    get_file_size(file_path) checks the file size at the dictionary 
    at file_path

    REQUIRES: file_path is the size of the file and is a JSON file
    HELPER METHOD FOR STUDENTS TO USE!
    """
    return os.path.getsize(file_path)


def log(file_path, new_dict, max_size):
    """
    log(file_path, new_dict) overwrites the data at old_dict
    at file_path if the combined memlry is greater than max_size. Does notRemoves
    duplicates if new_dict and old_dict shaare kesy for the new-dict's favor

    REQUIRES: file_path contains a dicitonary that is in JSon format
    REQUIRES: new_dict is a dictionary in JSoN format
    WARNING: DOWS NOT REMOVES DUPLICATES
    """
    old_size = get_file_size(file_path)
    new_size = old_size + sys.getsizeof(new_dict)
    if new_size > MAX_SIZE:
        # overwrite the memory location
        fp = open(file_path, "w")
        json.dump(new_dict, fp)
        fp.close()
    else:
        # append
        append_dict(file_path, new_dict)
