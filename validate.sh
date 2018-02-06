mkdir build
curl https://github.com/coreygirard/breeze-ci-example/archive/master.zip -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest
cp hello.py build/latest/hello.py

docker build -t breeze-latest .


text=`docker run breeze-latest`
echo "text is $? $text" 

rm -rf build

#rm build/latest/*
#rm build/latest/.gitignore
#rmdir build/latest
#rm build/latest.zip
