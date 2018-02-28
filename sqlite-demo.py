#!/usr/bin/env python
"""
http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
http://zetcode.com/db/sqlitepythontutorial/

http://www.sqlitetutorial.net/sqlite-python/
http://www.sqlitetutorial.net/sqlite-python/insert/
http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
"""
import os
import sqlite3
import hashlib

# ~~~~~ FUNCTIONS ~~~~~ #
def get_table_names(conn):
    """
    Gets all the names of tables in the database
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    names = cursor.fetchall()
    return(names)

def create_table(conn, table_name, col_name, col_type, is_primary_key = False):
    """
    Create a table if it doesnt exist with a starting column
    """
    cursor = conn.cursor()
    sql_cmd = 'CREATE TABLE IF NOT EXISTS {0}'.format(table_name)
    if is_primary_key:
        table_cmd = ' ({0} {1} PRIMARY KEY)'.format(col_name, col_type)
    else:
        table_cmd = ' ({0} {1})'.format(col_name, col_type)
    sql_cmd = sql_cmd + table_cmd
    print(sql_cmd)
    cursor.execute(sql_cmd)

def get_colnames(conn, table_name):
    """
    Gets the column names from a table
    """
    colnames = []
    sql_cmd = 'select * from {0}'.format(table_name)
    print(sql_cmd)
    cursor = conn.execute(sql_cmd)
    for item in cursor.description:
        colnames.append(item[0])
    return(colnames)

def add_column(conn, table_name, col_name, col_type, default_val = None):
    """
    Adds a column to a table
    """
    sql_cmd = "ALTER TABLE {0} ADD COLUMN '{1}' {2}".format(table_name, col_name, col_type)
    if default_val:
        default_val_cmd = " DEFAULT '{0}'".format(default_val)
        sql_cmd = sql_cmd + default_val_cmd
    print(sql_cmd)
    try:
        cursor = conn.cursor()
        cursor.execute(sql_cmd)
    except:
        # the column already exists...
        pass

def sqlite_insert(conn, table, row, ignore = False):
    cols = ', '.join('"{0}"'.format(col) for col in row.keys())
    vals = ', '.join(':{0}'.format(col) for col in row.keys())
    sql = 'INSERT '
    if ignore:
        sql = sql + 'OR IGNORE '
    sql = sql + 'INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    print(sql)
    conn.cursor().execute(sql, row)
    conn.commit()

def md5_str(item):
    """
    Gets the md5sum on the string representation of an object
    """
    try:
        # python 2.x
        md5 = hashlib.md5(str(item)).hexdigest()
    except:
        # python 3.x
        md5 = hashlib.md5(str(item).encode('utf-8')).hexdigest()
    return(md5)

def row_exists(conn, table_name, col_name, value):
    """
    Checks to see if a row exists in a table based on the provided criteria
    """
    sql_cmd = 'SELECT count(*) FROM {0} WHERE {1} = "{2}"'.format(table_name, col_name, value)
    print(sql_cmd)
    cursor = conn.execute(sql_cmd)
    data = cursor.fetchone()[0]
    if data == 0:
        return(False)
    else:
        return(True)





# ~~~~~ RUN ~~~~~ #
vals1 = ["foo", "bar", "baz"]
vals2 = ["foo", "fuz", "bar", "boz"]
vals_table_name = "vals"

vals_col1_name = "value"
vals_col1_type = "TEXT"

vals_col2_name = "key"
vals_col2_type = "TEXT"


db_file = "samples.sqlite"

# connect to db
conn = sqlite3.connect(db_file)
table_names = get_table_names(conn = conn)
table_names

# make the first table if it doesnt exist
create_table(conn = conn, table_name = vals_table_name, col_name = vals_col2_name, col_type = vals_col2_type, is_primary_key = True)
colnames = get_colnames(conn = conn, table_name = vals_table_name)
colnames

# add another column
add_column(conn = conn, table_name = vals_table_name, col_name = vals_col1_name, col_type = vals_col1_type)
colnames = get_colnames(conn = conn, table_name = vals_table_name)
colnames

# add all the values
for val in vals1:
    key = md5_str(val)
    row = {'key': key, 'value': val}
    sqlite_insert(conn = conn, table = vals_table_name, row = row, ignore = True)

# check if the new values aren't present..
not_present = []
present = []
for val in vals2:
    key = md5_str(val)
    if not row_exists(conn = conn, table_name = vals_table_name, col_name = "key", value = key):
        not_present.append((key, val))
    else:
        present.append((key, val))

print('not_present: {0}'.format(not_present))
print('present: {0}'.format(present))

conn.commit()
conn.close()
