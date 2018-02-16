FROM python:alpine

ADD /build/latest /src

RUN pip install coverage

ARG test_path
CMD [ "python", $test_path ]

CMD coverage run ./src/example/test_example.py; coverage annotate -d /report/; ls -p -R /src/ > /report/ls_report.txt
