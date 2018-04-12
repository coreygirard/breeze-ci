import os
import json
from flask import render_template, Markup


def fetch_data(user, repo, filename):
    with open(os.path.join('data', user, repo, 'recent.json'), 'r') as f:
        data = json.load(f)[filename]

    return data

def make_link_url(data):
    url = 'https://github.com/{0}/{1}/blob/{2}/{3}#L{4}'
    url = url.format(data['user'],
                     data['repo'],
                     data['hash'],
                     data['filepath'],
                     data['line_num'])
    return url

def make_line_code_span(status, code, url):
    if status == '>':
        color = 'green'
    elif status == '!':
        color = 'red'
    else:
        color = 'clear'

    code = code.replace(r' ', r'&nbsp')
    line = '<a href="{url}">{line}</a>'.format(url=url,
                                               line=code)
    line = '<span class="code-line line-{color}">{line}</span><br>'.format(color=color,
                                                                           line=line)
    return line

def make_line_num_span(data):
    n = len(str(data['max_line_num']))

    num = str(data['line_num']) + ' '*(n+1)
    num = num[:n+1].replace(r' ', r'&nbsp')
    num = '    <span class="number">{num}</span>'.format(num=num)
    return num

def build_code_line(data):
    num_span = make_line_num_span(data)

    url = make_link_url(data)
    code_span = make_line_code_span(data['status'],
                                    data['code'],
                                    url)

    return num_span + code_span






def build_report_header(filename):
    html = '''<h2><span style="font-family: 'PT Sans', sans-serif">{0}</span></h2>'''

    .format(data['filename'][4:])

def build_report(user, repo, filename):
    lines = []

    lines.append(
    for i, (a, b) in enumerate(data['lines'], start=1):
        num = (str(i)+' '*(max_num_len+1))[:max_num_len+1].replace(r' ', r'&nbsp')
        text = b.replace(r' ', r'&nbsp')
        lines.append(get_report_line(a, num, text))

    row = '<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}%</th></tr>'
    lines.append('<table>')
    red = data['stats'].get('!', 0)
    green = data['stats'].get('>', 0)
    percent = round(100*green/(red+green), 2)
    lines.append(row.format('''<span style="font-family: 'PT Sans', sans-serif">Total</span>''',
                            red, green, percent))
    lines.append('</table>')

    lines = Markup('\n'.join(lines))

    title = 'Breeze CI: {0}/{1}'.format(user, repo)

    return render_template('report_template.html',
                           title=title,
                           text=lines)















link = '<a href="/{user}/{repo}/{hash}">{text}</a><br>'
row = '<tr><th>{0}</th><th>{1}</th><th>{2}</th><th>{3}%</th></tr>'
def build_index(user, repo):
    with open(os.path.join('data', user, repo, 'recent.json'), 'r') as f:
        data = json.load(f)

    temp = []
    for h, e in data.items():
        if h == 'overall':
            continue

        red = e['stats'].get('!', 0)
        green = e['stats'].get('>', 0)
        percent = round(100*green/(red+green), 2)

        link_built = link.format(user=user,
                                 repo=repo,
                                 hash=h,
                                 text=e['filename'][4:])
        row_built = row.format(link_built,
                               red,
                               green,
                               percent)

        temp.append(row_built)

    all_red = data['overall']['stats'].get('!', 0)
    all_green = data['overall']['stats'].get('>', 0)
    all_percent = round(100*all_green/(all_red+all_green), 2)
    temp.append(row.format('Overall',
                           all_red,
                           all_green,
                           all_percent))

    temp = Markup('\n'.join(temp))

    header = ''.join(['''<h2><span style="font-family: 'PT Sans', sans-serif">''',
                      '''<a href="https://www.github.com/{0}">{0}</a> / ''',
                      '''<a href="https://www.github.com/{0}/{1}">{1}</a>''',
                      '''</span></h2>'''])
    header = header.format(user, repo)
    header = Markup(header)

    title = 'Breeze CI: {0}/{1}'.format(user, repo)

    return render_template('index_template.html',
                           title=title,
                           userrepo=header,
                           table=temp)
