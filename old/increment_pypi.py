import sys
import re

def increment(e):
    e = e.strip(' ')
    e = e.split('.')
    e[-1] = str(int(e[-1])+1)
    return '.'.join(e)

def loadfile(path):
    with open(path,'r') as f:
        text = f.read()
    return text

def savefile(path,text):
    with open(path,'w') as f:
        f.write(text)

def increment_version_number(filepath):
    pattern = "(?<=version=')([ .0-9]+?)(?=')"
    match = list(re.finditer(pattern,text))[0]

    start,stop = match.span()
    payload = match.group()

    payload = increment(payload)

    return text[:start]+payload+text[stop:]

path = sys.argv[1]
text = loadfile(path)
text = increment_version_number(text)
print(text)
savefile(path,text)
