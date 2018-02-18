from flask import Flask, request, render_template, Markup, jsonify
import os
import random
import json
import re
from pprint import pprint



link = '<a href="/{user}/{repo}/{hash}">{text}</a><br>'
row = '<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}%</th></tr>'
def build_index(user, repo):
    with open(os.path.join('data', user, repo, 'recent.json'), 'r') as f:
        data = json.load(f)

    temp = []
    for h,e in data.items():
        if h == 'overall':
            continue

        red = e['stats'].get('!', 0)
        green = e['stats'].get('>', 0)
        percent = round(100*green/(red+green), 2)

        link_built = link.format(user=user,
                                 repo=repo,
                                 hash=h,
                                 text=e['filename'])
        row_built = row.format(link_built,
                               red,
                               green,
                               percent)

        temp.append(row_built)

    all_red = data['overall']['stats'].get('!',0)
    all_green = data['overall']['stats'].get('>',0)
    all_percent = round(100*all_green/(all_red+all_green), 2)
    temp.append(row.format('Overall',
                           all_red,
                           all_green,
                           all_percent))

    temp = Markup('\n'.join(temp))

    header = '<h3><a href="https://www.github.com/{0}">{0}</a>' + \
             ' / <a href="https://www.github.com/{0}/{1}">{1}</a>' + \
             '</h3>'
    header = header.format(user, repo)
    header = Markup(header)

    return render_template('index_template.html', userrepo=header, table=temp)


lookup = {'>':'    <span style="font-family: Inconsolata, Courier New;">{0}</span>'
              '<span style="font-family: Inconsolata, Courier New; background-color:#a5d6a7">{1}</span><br>',
          '!':'    <span style="font-family: Inconsolata, Courier New;">{0}</span>'
              '<span style="font-family: Inconsolata, Courier New; background-color:#ef9a9a">{1}</span><br>',
          ' ':'    <span style="font-family: Inconsolata, Courier New;">{0}</span>'
              '<span style="font-family: Inconsolata, Courier New;">{1}</span><br>'}
def build_report(user, repo, filename):
    with open(os.path.join('data', user, repo, 'recent.json'), 'r') as f:
        data = json.load(f)[filename]

    # using this method because calc via log had floating point problems
    max_num_len = 1
    while 10**max_num_len < len(data['lines']):
        max_num_len += 1

    lines = []

    #lines.append('''<h2><span style="font-family: 'PT Sans Narrow', sans-serif">/src/example/example.py</span></h2>''')
    lines.append('''<h2><span style="font-family: 'PT Sans', sans-serif">/src/example/example.py</span></h2>''')
    #lines.append('''<h2><span style="font-family: 'Oswald', sans-serif">/src/example/example.py</span></h2>''')
    for i,(a,b) in enumerate(data['lines'], start=1):
        num = (str(i)+' '*(max_num_len+1))[:max_num_len+1].replace(r' ',r'&nbsp')
        text = b.replace(r' ',r'&nbsp')
        lines.append(lookup[a].format(num,text))

    row = '<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}%</th></tr>'
    lines.append('<table>')
    red = data['stats'].get('!', 0)
    green = data['stats'].get('>', 0)
    percent = round(100*green/(red+green), 2)
    lines.append(row.format('''<span style="font-family: 'PT Sans', sans-serif">Total</span>''', 
                            red, green, percent))
    lines.append('</table>')

    lines = Markup('\n'.join(lines))

    return render_template('report_template.html', text=lines)
