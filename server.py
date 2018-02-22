from flask import Flask, request, render_template, Markup, jsonify
import os
import random
import json
import re
from pprint import pprint
import render
import generate

app = Flask(__name__)


@app.route('/<user>/<repo>')
@app.route('/<user>/<repo>/')
def repo(user, repo):
    try:
        return render.build_index(user, repo)
    except:
        return "404"

@app.route('/<user>/<repo>/<filename>')
def repo_file(user, repo, filename):
    try:
        return render.build_report(user, repo, filename)
    except:
        return "404"


@app.route('/webhook', methods=['POST'])
def hook():
    j = request.get_json()
    return generate.from_webhook(path='./',
                                 data=j)

if __name__ == '__main__':
    app.run(debug=True)
