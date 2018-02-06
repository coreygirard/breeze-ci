FROM python:alpine

ADD /build/latest /

#RUN pip install pystrich

ARG test_path
#CMD [ "python", "./example/test_example.py" ]
