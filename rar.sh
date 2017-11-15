#!/bin/bash

# how to archive files with rar on macOS
# get rar from here:
# https://www.rarlab.com/download.htm
# https://www.rarlab.com/rar/rarosx-5.5.0.tar.gz

printf 'do not run this script directly you need to configure the rar bin path\n'
cat "$0"
exit

# this is the command to rar a dir
# example dir:
# dir
# |-- foo.txt
# |-- bar.txt
# |-- subdir1
# |   `-- foo.txt
# `-- subdir2
#     `-- foo.txt

# use this command
# rar/rar a -ep1 -r -ppassword my_archive.rar /path/to/dir
