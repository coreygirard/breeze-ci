FROM python:alpine

ADD /build/latest /

#RUN pip install pystrich

CMD [ "python", "./hello.py" ]
