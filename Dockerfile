FROM python:alpine

ADD /build/latest /

RUN pip install coverage

    #mv temp.txt shared
    #touch ./shared/temp.txt

ARG test_path
CMD [ "python", "--version" ]
CMD python --version
    #[ "ls" ] #[ "echo", "Hello World" ] #> temp.txt
