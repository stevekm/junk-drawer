#!/usr/bin/env python
# python 2.7

# have: txt files containing lists of files in the following format:
# <md5sum>    /file/path/file.txt
# need to compare two files to see which entries in one 
# are missing in the other

import collections

def get_entries(file_path, head = False):
    # get entries on each line of a file, delimited by first whitespace
    entry_list = []
    with open(file_path, 'r') as f:
        if head:
            lines = [next(f) for x in xrange(head)]
        else:
            lines = f
        for line in lines:
            entries = line.split(None, 1)
            entry_list.append(entries)
    return entry_list

def make_entries_dict(file_path, *args, **kwargs):
    # make a dict out of the entries gathered from the file
    entries_dict = collections.defaultdict(list)
    for key, entry in  get_entries(file_path, *args, **kwargs):
        entries_dict[key].append(entry)
    return entries_dict

home_files_txt = "/Users/steve/home_files.txt"
backup_files_txt = "/Users/steve/Orchard_files.txt"

home_dict = make_entries_dict(home_files_txt)
backup_dict = make_entries_dict(backup_files_txt)

unmatched_keys = [key for key in home_dict.keys() if not key in backup_dict.keys()]
# filtered = [i for i in a if not i[0] in b]

# print unmatched_keys

for key in unmatched_keys: 
    item = home_dict[key]
    print item[0]


# for key, entry in files_dict.items():
#     print key, entry
