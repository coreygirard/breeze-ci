from flask import Flask, request, render_template, Markup
import os
import random
import json
import re
from pprint import pprint


app = Flask(__name__)

@app.route('/<user>/<repo>')
def repo(user, repo):
    with open('report/ls_report.txt', 'r') as f:
        text = f.read()
    return text
    return user + '///' + repo

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



@app.route('/webhook', methods=['POST'])
def hook():
    j = request.get_json()
    data = {'repository': {'name':                 j['repository']['name'],
                           'full_name':            j['repository']['full_name'],
                           'owner': {'login':      j['repository']['owner']['login'],
                                     'avatar_url': j['repository']['owner']['avatar_url'],
                                     'html_url':   j['repository']['owner']['html_url']},
                           'private':              j['repository']['private'],
                           'html_url':             j['repository']['html_url'],
                           'pushed_at':            j['repository']['pushed_at']},
            'sender': {'login':                    j['sender']['login'],
                       'avatar_url':               j['sender']['avatar_url'],
                       'html_url':                 j['sender']['html_url']}}
    pprint(data)
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
