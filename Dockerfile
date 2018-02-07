FROM python:alpine

ADD /build/latest /src

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]

CMD coverage run /src/example/test_example.py
CMD coverage annotate -d /src/example/

CMD echo "hey" > hello.txt,cover

CMD echo "hello from Docker" > test.txt
