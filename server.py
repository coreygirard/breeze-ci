from flask import Flask, request, render_template, Markup, jsonify
import os
import random
import json
import re
from pprint import pprint


app = Flask(__name__)


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


lookup = {'>':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New; background-color:#a5d6a7">{1}</span><br>',
          '!':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New; background-color:#ef9a9a">{1}</span><br>',
          ' ':'    <span style="font-family: Courier New;">{0}</span>'
              '<span style="font-family: Courier New;">{1}</span><br>'}
def build_report(user, repo, filename):
    with open(os.path.join('data', user, repo, 'recent.json'), 'r') as f:
        data = json.load(f)

    try:
        data = data[filename]
    except:
        return "404"

    lines = []
    # using this method because calc via log had floating point problems
    max_num_len = 1
    while 10**max_num_len < len(data['lines']):
        max_num_len += 1

    for i,(a,b) in enumerate(data['lines'], start=1):
        num = (str(i)+' '*(max_num_len+1))[:max_num_len+1].replace(r' ',r'&nbsp')
        text = b.replace(r' ',r'&nbsp')
        lines.append(lookup[a].format(num,text))

    lines = Markup('\n'.join(lines))

    return render_template('report_template.html', text=lines)


def to_html(rep):
    lines = []
    lines = '\n'.join(lines)


@app.route('/<user>/<repo>')
@app.route('/<user>/<repo>/')
def repo(user, repo):
    return build_index(user, repo)

@app.route('/<user>/<repo>/<filename>')
def repo_file(user, repo, filename):
    return build_report(user, repo, filename)




'''
#@app.route('/', methods=['POST'])
@app.route('/home')
def home():
    return render_template('index.html')

#@app.route('/', methods=['GET'])
@app.route('/file/<filename>')
def source(filename):
    try:
        return render_template(filename)
    except:
        return "404"
'''










def get_repo_info(j):
    repo = j['repository']
    owner = j['repository']['owner']
    return {'name': repo['name'],
            'private': repo['private'],
            'url': repo['html_url'],
            'owner_name': owner['name'],
            'owner_email': owner['email'],
            'owner_avatar': owner['avatar_url'],
            'owner_url': owner['html_url']}

def get_commit_info(j):
    temp = j['head_commit']
    return {'id': temp['id'],
            'message': temp['message'],
            'timestamp': temp['timestamp'],
            'url': temp['url'],
            'committer_name': temp['committer']['name'],
            'committer_email': temp['committer']['email'],
            'committer_username': temp['committer']['username'],
            'committer_url': j['sender']['html_url'],
            'committer_avatar': j['sender']['avatar_url']}

@app.route('/webhook', methods=['POST'])
def hook():
    j = request.get_json()
    #pprint(j)
    data = {'repo': get_repo_info(j),
            'commit': get_commit_info(j)}
    pprint(data)

    os.system('./val.sh "{0}"'.format(data['repo']['url']))

    path = '/Users/coreygirard/Documents/GitHub/breeze-ci/'
    user, repo = data['repo']['owner_name'], data['repo']['name']
    os.system('mkdir "{0}"'.format(os.path.join(path, 'data', user)))
    os.system('mkdir "{0}"'.format(os.path.join(path, 'data', user, repo)))
    cmd = '{0} {1} "{2}" "{3}" "{4}" "{5}"'.format('python3',
                                             'generate_report_json.py',
                                             path,
                                             user,
                                             repo,
                                             data['commit']['id'])
    os.system(cmd)
    os.system('rm -rf "{0}"'.format(os.path.join(path, 'report')))


    return "200"

if __name__ == '__main__':
    app.run(debug=True)

{
  "repository": {
    "name": "breeze-ci-example",
    "full_name": "coreygirard/breeze-ci-example",
    "owner": {
      "login": "coreygirard",
      "avatar_url": "https://avatars2.githubusercontent.com/u/4074644?v=4",
      "html_url": "https://github.com/coreygirard"
    },
    "private": false,
    "html_url": "https://github.com/coreygirard/breeze-ci-example",
    "pushed_at": "2018-02-14T21:26:45Z"
  },
  "sender": {
    "login": "coreygirard",
    "avatar_url": "https://avatars2.githubusercontent.com/u/4074644?v=4",
    "html_url": "https://github.com/coreygirard"
  }
}
