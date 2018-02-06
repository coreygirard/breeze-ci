rm -rf build

mkdir build
mkdir build/shared

curl https://github.com/coreygirard/breeze-ci-example/archive/master.zip -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest
#cp hello.py build/latest/hello.py

read -d $'\x04' TEST_PATH < "./build/latest/breeze.yml"
echo "Executing tests from: $TEST_PATH"
docker build -t --build-arg test_path="$TEST_PATH" breeze-latest .
docker run -v "$PWD/build/shared:/shared" breeze-latest

TEST_RESULT=$?
if [ $TEST_RESULT -eq "0" ]; then
  echo "Tests passed. Deploying..."
else
  echo "Tests failed. Not deploying."
fi

#rm -rf build
