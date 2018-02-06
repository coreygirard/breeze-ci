FROM python:alpine

ADD /build/latest /

#RUN pip install pystrich

CMD [ "python", "./test_example.py" ]
