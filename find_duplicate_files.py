#!/usr/bin/env python
# python 2.7

# find duplicate file entries from a text file formatted as such:
# <md5sum>    /file/path/file.txt

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

def get_duplicates(file_path, *args, **kwargs):
    files_dict = make_entries_dict(file_path, *args, **kwargs)
    # print files_dict
    dupes_dict = {}
    for key, value in files_dict.iteritems():
        print key, value
        if len(value) > 1:
            dupes_dict[key] = value
    return dupes_dict

def print_dict(some_dict, value_only = False):
    for key, value in some_dict.items():
        for item in value:
            if value_only:
                print item,
            else:
                print key, item,


file_list_txt = "/Users/steve/home_files_sort.txt"

print_dict(get_duplicates(file_list_txt, head = 500), value_only = True)


