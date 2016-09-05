#!/usr/bin/env python
# python 2.7

# a collection of some of my custom functions and code samples I've found useful

import sys
import os
import errno
import pandas as pd
import numpy as np
import fnmatch
import re
import subprocess as sp
import csv
import collections
import pickle
import argparse


# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def mkdir_p(path, return_path=False):
    # if not os.path.exists(dir_path):
    # os.makedirs(dir_path)
    # distutils.dir_util.mkpath(name[, mode=0777, verbose=0, dry_run=0])
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    if return_path:
        return path

def subprocess_cmd(command):
    # proc = sp.Popen(['ls','-l'])
    process = sp.Popen(command,stdout=sp.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

def get_file_path(search_dir='.',name='',path='', more=''):
    # print 'Searching for file:\t', name, '\nIn location:\t', search_dir + path
    filepath = [line for line in sp.check_output("find {} -name '{}' -path '{}'{}".format(search_dir,name,path,more), shell=True).splitlines()]
    return filepath[0] # return first result


def unzip_input_files(path):
    # find and unzip all .zip, .gz files
    # print path
    subprocess_cmd('cd "{}" && find . -name "*.zip" -exec unzip -n {{}} \; && $(for file in *.gz; do [ ! -f "${{file%%.gz}}" ] && gunzip "$file"; done)'.format(path))


def convert_2_annovar(vcf_input_file, av_output_file):
    if not os.path.exists(av_output_file) and not os.path.isfile(av_output_file):
        subprocess_cmd('convert2annovar.pl -format vcf4old {} -includeinfo > {}'.format(vcf_input_file,av_output_file))


def annovar_table(avinput, annovar_output, annovar_db_dir="/ifs/home/kellys04/software/annovar/db", build_version="hg19", annovar_protocol="-protocol refGene,cosmic68,clinvar_20150629,1000g2015aug_all -operation g,f,f,f"
):
    # avinput : file path to avinput
    # annovar_output : file path to annovar output
    #  --otherinfo # http://annovar.openbioinformatics.org/en/latest/user-guide/startup/
    file_suffix = '.' + build_version + '_multianno.txt'
    output_file = annovar_output + file_suffix
    if not os.path.exists(output_file) and not os.path.isfile(output_file):
        print "\nRunning ANNOVAR annotation on:\n", avinput
        subprocess_cmd('table_annovar.pl {} {} -buildver {} -out {} -remove {} -nastring .'.format(avinput, annovar_db_dir, build_version, annovar_output, annovar_protocol))
    # file.endswith('multianno.txt') # TSVC_variants_IonXpress_015_filtered.hg19_multianno.txt
    output_path = get_file_path(search_dir=os.path.dirname(output_file), name='*{}*'.format(os.path.basename(output_file)), path='*')
    print "\nAnnotated file is:\n", output_path
    return output_path


def vcf_header_skip(file_path):
    skip_rows = 0
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('##'):
                skip_rows += 1
            else:
                break
    return skip_rows

def vcf_qual_filter(vcf_table, qual_score = 250):
    # QUAL > 100 # df.loc[df['column_name'] == some_value]
    filtered_table = vcf_table.loc[vcf_table['QUAL'] > qual_score]
    return filtered_table


def av_table_filter(av_table, gene_func = "exonic", exonic_func_remove = "synonymous SNV", maf_cutoff = 0.01):
    # Func.refGene : exonic
    # ExonicFunc.refGene : synonymous SNV
    # 1000g2015aug_all : < 0.01 OR NA
    filtered_table = av_table.loc[ (av_table['ExonicFunc.refGene'] != exonic_func_remove) & ((av_table['1000g2015aug_all'] < maf_cutoff) | pd.isnull(av_table['1000g2015aug_all'])) & (av_table['Func.refGene'] == gene_func) ]
    return filtered_table

def xls_table_filter(xls_table, strand_bias_cutoff = 0.8, frequency_cutoff = 5):
    # Strand Bias < 0.8
    # Frequency > 5 
    # 1000g2015aug_all : < 0.01
    filtered_table = xls_table.loc[ (xls_table['Strand Bias'] < strand_bias_cutoff) & (xls_table['Frequency'] > frequency_cutoff)]
    return filtered_table

def key0(data):
    # return the first key in the data; convenience function for code truncation
    key_0 = data.keys()[0]
    return key_0

def val0(data):
    # return the first value in the data; convenience function for code truncation
    value0 = data.values()[0]
    return value0

def custom_table_filter(dataframe, gene_func_include = ['Func.refGene', 'exonic'], 
    exonic_func_remove = ['ExonicFunc.refGene', 'synonymous SNV'], maf_cutoff_upper = ['1000g2015aug_all', 0.01],
    strand_bias_cutoff_upper = ['Strand Bias', 0.8], frequency_cutoff_lower = ['Frequency', 5]): 
    # gene_func_include -  list, [colname, value] for inclusion
    #
    # apply filters to the df
    filtered_df = dataframe.loc[ ( dataframe[gene_func_include[0]] == gene_func_include[1] ) &
    ( dataframe[exonic_func_remove[0]] != exonic_func_remove[1] ) &
    ( ( dataframe[maf_cutoff_upper[0]] < maf_cutoff_upper[1] ) | pd.isnull(dataframe[maf_cutoff_upper[0]]) ) &
    ( dataframe[strand_bias_cutoff_upper[0]] < strand_bias_cutoff_upper[1]) &
    ( dataframe[frequency_cutoff_lower[0]] > frequency_cutoff_lower[1]) ]
    return filtered_df


def save_pydata(data, outfile):
    with open(outfile, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print 'Object saved to file:\n', outfile



def load_pydata(infile):
    with open(infile, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)
        return data

def split_df_col2rows(dataframe, split_col, split_char, new_colname, delete_old = False, reset_indexes = True):
    # # Splits a column into multiple rows # # import pandas as pd
    # dataframe : pandas dataframe to be processed
    # split_col : chr string of the column name to be split
    # split_char : chr to split the col on
    # new_colname : new name for the 
    # delete_old : logical True / False, remove original column?
    # ~~~~~~~~~~~~~~~~ # 
    # save the split column as a separate object
    tmp_col = dataframe[split_col].str.split(split_char).apply(pd.Series, 1).stack()
    # drop the last index level
    tmp_col.index = tmp_col.index.droplevel(-1)
    # set the new col name
    tmp_col.name = new_colname
    # remove the original column from the df
    if delete_old is True:
        del dataframe[split_col]
    # join them into a new df 
    new_df = dataframe.join(tmp_col)
    if reset_indexes is True:
        new_df = new_df.reset_index(drop=True)
    return new_df


def split_df_col2cols(dataframe, split_col, split_char, new_colnames, delete_old = False):
    # # Splits a column into multiple columns # # import pandas as pd
    # dataframe : pandas dataframe to be processed
    # split_col : chr string of the column name to be split
    # split_char : chr to split the col on
    # new_colnames : list of new name for the columns
    # delete_old : logical True / False, remove original column?
    # ~~~~~~~~~~~~~~~~ # 
    # save the split column as a separate object
    new_cols = dataframe[split_col].str.split(split_char).apply(pd.Series, 1)
    # rename the cols
    new_cols.columns = new_colnames
    # remove the original column from the df
    if delete_old is True:
        del dataframe[split_col]
    # merge with df
    new_df = dataframe.join(new_cols)
    return new_df

def av_df_fixcolnames(av_df):
    # print "GOT THE DATA, looks like this:\n", av_df.keys()
    # # reformat the ANNOVAR dataframe for merging
    # Bad:Good
    fix_colnames = {'Ref':'Ref', 'Alt':'Variant', 'Chr':'Chrom', 'Start':'Position'}
    # replace the bad colnames with the good ones for merging
    for i in range(0,len(fix_colnames)):
        bad_colname = fix_colnames.keys()[i]
        # print bad_colname
        #
        good_colname = fix_colnames[fix_colnames.keys()[i]]
        # print good_colname
        # print bad_colname, " : ", good_colname
        # print {bad_colname:good_colname}
        av_df = av_df.rename(columns = {bad_colname:good_colname})
    # print "CHANGED COLNAMES, looks like this:\n", av_df.keys()
    # make sure they are all caps for merging
    av_df['Ref'] = av_df['Ref'].str.upper()
    av_df['Variant'] = av_df['Variant'].str.upper()
    return av_df

def partial_reorder_list(old_list, reference_list, verbose = False):
    # put the entries in the reference list at the front of the old list, if present
    if verbose is True:
        print '\nOld list contents:\n', old_list
    i = 0
    for entry in reference_list:
        if entry in old_list:
            old_list.insert(i, old_list.pop(old_list.index(entry)))
            i += 1
    if verbose is True:
        print '\nNew list contents:\n', old_list
    return old_list

def list_file_lines(file_path):
    # not blank lines, no trailing \n
    with open(file_path, 'r') as f:
        entries = [line.strip() for line in f if line.strip()]
    return entries

def shell_unzip(file, outdir = '.'):
    subprocess_cmd('unzip -n {} -d {}'.format(file,outdir))

def shell_gunzip(file):
    subprocess_cmd('file="{}"; [ ! -f "${{file%%.gz}}" ] && gunzip {}'.format(file,file))

def pipeline_unzip(input_file, outdir):
    # unzip the input file
    if input_file.endswith('.zip'): shell_unzip(input_file,outdir = outdir)
    # find and unzip the .gz files extracted
    for subdir, dirs, files in os.walk(outdir):
        for file in files:
            if file.endswith('.gz'):
                # print os.path.join(subdir,file)
                shell_gunzip(os.path.join(subdir,file))

def pipeline_concat_sampledata(samples_dict):
    summary_table = pd.concat([samples_dict[sample]['merged_dataframe'] for sample in samples_dict.keys()], join = 'outer')
    return summary_table


# ~~~~ GET SCRIPT ARGS ~~~~~~ #
# python test.py arg1 arg2 arg3
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
# print 'script name is:', sys.argv[0]
parser = argparse.ArgumentParser(description='IonTorrent annotation pipeline.')
parser.add_argument("input_files",help="Path to input files; .zip IonTorrent run files", nargs=2)
parser.add_argument("-o", help="Path to output directory. Defaults to the current directory", default = '.', type = str, dest = 'output')
parser.add_argument("-id", help="Run ID value. Defaults to the portion of the input filename preceeding the first '.' character ")
args = parser.parse_args()

print 'outdir is:', args.output

# create a dict of dicts to hold information on the input files
run_dict = collections.defaultdict(dict)
