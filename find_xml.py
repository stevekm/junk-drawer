#!/usr/bin/env python

import os

def find_H_dirs(parent_dir):
    '''
    Find all the dirs in the parent_dir that start with H
    '''
    matches = []
    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        if os.path.isdir(item) & item.startswith("H"):
            matches.append(item_path)
    return(matches)

def find_XML_files(dir):
    '''
    Find all the .xml files in a dir
    '''
    matches = []
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        if os.path.isfile(item_path) & item.endswith(".xml"):
            matches.append(item_path)
    return(matches)

def process_XML_file(XML_file, output_handle):
    '''
    Do a thing to the XML file
    '''
    print("Put your code for processing the {0} file here.".format(XML_file))


# parent_dir = "/path/to/parent_dir"
parent_dir = "."
# output_handle = "/path/to/my_data_parse.xml" # if you want it to always go to the same file

H_dirs = find_H_dirs(parent_dir = parent_dir)

for H_dir in H_dirs:
    output_handle = os.path.join(H_dir, "my_data_parse.xml")
    for XML_file in find_XML_files(dir = H_dir):
        process_XML_file(XML_file = XML_file, output_handle = output_handle)
