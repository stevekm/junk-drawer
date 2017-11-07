#!/usr/bin/env python

'''
python 3.6+

extract each file from .zip
write to a new .zip, in its own folder
'''
import os
from zipfile import ZipFile, ZIP_DEFLATED

src_zip = os.path.join("pics", "cats.zip")
dst_zip = os.path.join('out', 'new.zip')

with ZipFile(src_zip, "r", compression = ZIP_DEFLATED) as src_zip_archive:
    with ZipFile(dst_zip, "w", compression=ZIP_DEFLATED) as dst_zip_archive:
        for zitem in src_zip_archive.namelist():
            # read bytes from zip file
            src = src_zip_archive.read(zitem)
            # create output archive filepath; file/file.txt
            nm = os.path.join(os.path.splitext(zitem)[0], zitem)
            # write to the output archive
            dst_zip_archive.writestr(nm, src)
