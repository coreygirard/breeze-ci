FROM python:alpine

ADD /build/latest /src
ADD /build/latest/example /

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]

#CMD ll

#CMD cd /src/example
#CMD echo "hey" > testing.txt
#CMD coverage run test_example.py
#CMD coverage annotate -d .
#CMD ../..

#CMD cat /src/example/test_example.py
#CMD cat /src/example/test_example.py > ./test_example.py

CMD coverage run ./test_example.py
CMD coverage annotate -d ./

CMD echo "graffiti graffiti graffiti" > ./test_example.py

#CMD chmod 777 ./src/example
#CMD echo "hey" > ./src/example/hello.txt

#CMD mkdir report
CMD echo "hello from Docker" > ./test.txt
