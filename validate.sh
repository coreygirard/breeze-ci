mkdir build
curl https://github.com/coreygirard/breeze-ci-example/archive/master.zip -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest
cp hello.py build/latest/hello.py

docker build -t breeze-latest .
docker run breeze-latest

TEST_RESULT=$?
echo "result: $?"

if [ $TEST_RESULT -eq "0" ]; then
  echo "Tests passed. Deploying..."
else
  echo "Tests failed. Not deploying."
fi

rm -rf build
