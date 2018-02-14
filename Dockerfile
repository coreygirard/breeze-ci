FROM python:alpine

ADD /build/latest /src
ADD /build/latest/example /

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]

#CMD coverage run ./test_example.py
#CMD sudo coverage annotate -d ./

#CMD chmod 777 ./src/example
#CMD echo "hey" > ./src/example/hello.txt

#CMD echo "hello from Docker" > ./test.txt

CMD coverage run ./test_example.py; coverage annotate -d /report/
