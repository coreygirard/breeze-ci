from flask import Flask, request, render_template, Markup
import os
import random
import json
import re


app = Flask(__name__)


#@app.route('/', methods=['POST'])
@app.route('/home')
def home():
    return render_template('index.html')

#@app.route('/', methods=['GET'])
@app.route('/file/<filename>', methods=['GET'])
def source(filename):
    return render_template(filename)

if __name__ == '__main__':
    app.run(debug=True)
