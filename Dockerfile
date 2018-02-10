FROM python:alpine

ADD /build/latest /src

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]

#CMD cd /src/example
#CMD echo "hey" > testing.txt
#CMD coverage run test_example.py
#CMD coverage annotate -d .
#CMD ../..

CMD cat /src/example/test_example.py
CMD cat /src/example/test_example.py > ./test_example.py

#CMD coverage run /src/example/test_example.py
#CMD coverage annotate -d /src/example/

#CMD echo "hey" > ./hello.txt,cover

#CMD mkdir report
CMD echo "hello from Docker" > ./test.txt
