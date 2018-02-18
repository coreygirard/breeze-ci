import os
import sys
import re
from pprint import pprint
import json
import hashlib

def make_rename_lookup(raw_path):
    d = {}

    with open(os.path.join(raw_path, 'ls_report.txt')) as f:
        lines = [line.strip('\n') for line in f]

    indices = [i for i,e in enumerate(lines) if e == '']
    indices = [-1] + indices + [len(lines)]

    lines = [lines[a+1:b] for a, b in zip(indices,indices[1:])]
    for e in lines:
        a, b = e[0], e[1:]

        while a[-1] in '/:':
            a = a[:-1]
        a = a + '/'

        for i in b:
            filepath = a+i
            d[filepath.replace('/','_')] = filepath

    return d

def is_covered(r):
    return [(e[0],e[2:]) for e in r]

def get_raw_reports(path):
    report = {}
    for filename in os.listdir(path):
        if not filename.endswith(',cover'):
            continue
        else:
            savename = filename[:-6]

        filepath = os.path.join(path,filename)
        savepath = os.path.join(path,savename)

        with open(filepath,'r') as f:
             temp = [line.strip('\n') for line in f]
             report[savename] = is_covered(temp)
    return report

def to_stats(rep):
    d = {}
    for e,_ in rep:
        if e != ' ':
            d[e] = d.get(e,0)+1
    return d


def collate_data(path, user, repo, commit):
    reports = get_raw_reports(os.path.join(path, 'report'))
    rename_lookup = make_rename_lookup(os.path.join(path, 'report'))




    data = {}
    for k,v in reports.items():
        h = hashlib.md5(k.encode('utf-8')).hexdigest()

        filename = rename_lookup[k]
        data[h] = {'filename': filename,
                   'lines': v,
                   'stats': to_stats(v)}

    overall = {}
    for e in data.values():
        for k,v in e['stats'].items():
            overall[k] = overall.get(k, 0) + v
    data['overall'] = {'stats': overall}

    with open(os.path.join(path, 'data', user, repo, 'recent.json'), 'w') as f:
        json.dump(data, f, indent=4)
    with open(os.path.join(path, 'data', user, repo, '{0}.json'.format(commit)), 'w') as f:
        json.dump(data, f, indent=4)


path = sys.argv[1]
user = sys.argv[2]
repo = sys.argv[3]
commit = sys.argv[4]

#path = '/Users/coreygirard/Documents/GitHub/breeze-ci/'
#user = 'coreygirard'
#repo = 'breeze-ci-example'
collate_data(path, user, repo, commit)
# python3 generate_report_json.py "/Users/coreygirard/Documents/GitHub/breeze-ci/" "coreygirard" "breeze-ci-example"
