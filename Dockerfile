FROM python:alpine

ADD latest /

#RUN pip install pystrich

CMD [ "python", "./hello.py" ]
