import os
import sys
import re
from pprint import pprint


def is_covered(r):
    return [(e[0],e[2:]) for e in r]

def get_raw_reports(path):
    report = {}
    for filename in os.listdir(path):
        if not filename.endswith(',cover'):
            continue
        else:
            savename = filename[:-6]+'.html'

        filepath = os.path.join(path,filename)
        savepath = os.path.join(path,savename)
        with open(filepath,'r') as f:
             temp = [line.strip('\n') for line in f]
             report[savename] = is_covered(temp)
    return report

lookup = {'>':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New; background-color:#a5d6a7">{1}</span><br>',
          '!':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New; background-color:#ef9a9a">{1}</span><br>',
          ' ':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New;">{1}</span><br>'}
def to_html(rep):
    with open('/Users/coreygirard/Documents/GitHub/breeze-ci/data/report_template.html', 'r') as f:
        template = f.read()

    lines = []
    for i,(a,b) in enumerate(rep, start=1):
        num = (str(i)+' '*10)[:3].replace(r' ',r'&nbsp')
        text = b.replace(r' ',r'&nbsp')
        lines.append(lookup[a].format(num,text))
    lines = '\n'.join(lines)

    return template.replace('{{text}}', lines)

def to_stats(rep):
    d = {}
    for e,_ in rep:
        if e != ' ':
            d[e] = d.get(e,0)+1
    return d



link = '<a href="/file/{0}">{1}</a><br>'
row = '<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}%</th></tr>'
def build_main(stats):
    with open('/Users/coreygirard/Documents/GitHub/breeze-ci/data/index_template.html', 'r') as f:
        template = f.read()

    temp = []
    for k,v in stats.items():
        red = v.get('!', 0)
        green = v.get('>', 0)
        percent = round(100*green/(red+green), 2)

        link_built = link.format(k,k)
        row_built = row.format(link_built,
                               red,
                               green,
                               percent)

        temp.append(row_built)
    temp = '\n'.join(temp)

    return template.replace('{{table}}', temp)

raw_path = '/Users/coreygirard/Documents/GitHub/breeze-ci/report/'
'''
template_path = '/Users/coreygirard/Documents/GitHub/breeze-ci/templates/'
reports = get_raw_reports(raw_path)

stats = {k:to_stats(v) for k,v in reports.items()}
html = {k:to_html(v) for k,v in reports.items()}

#pprint(stats)
#pprint(html)
#print(list(html.values())[0])


main = build_main(stats)
with open(os.path.join(template_path, 'index.html'), 'w') as f:
    f.write(main)

for k,v in html.items():
    with open(os.path.join(template_path, k), 'w') as f:
        f.write(v)
'''



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

pprint(d)
