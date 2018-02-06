FROM python:alpine

ADD /build/latest /

#RUN pip install pystrich

ARG test_path
CMD [ "python", "./hello.py" ]
