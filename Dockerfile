FROM python:alpine

ADD /build/latest /src

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]
CMD echo "hello from Docker" > test.txt
