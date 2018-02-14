REPO="https://github.com/coreygirard/breeze-ci-example/archive/master.zip"

rm -rf build
rm -rf dump
rm -rf report

mkdir build
mkdir build/shared
mkdir report

curl "$REPO" -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest

read -d $'\x04' TEST_PATH < "./build/latest/breeze.yml"
echo "Executing tests from: $TEST_PATH"

docker rm breeze-container
docker rmi breeze-image

docker build -t breeze-image -f "./Dockerfile" --no-cache --build-arg test_path="$TEST_PATH" ./
docker run -d --name breeze-container -v $(pwd)/report:/report -i -t breeze-image

TEST_RESULT=$?
echo "Received: $TEST_RESULT"
if [ $TEST_RESULT -eq "0" ]; then
  echo "Tests passed. Deploying..."

  python3 increment_pypi.py build/latest/setup.py
  cd build/latest
  python setup.py sdist bdist_wheel
  cd ../..
else
  echo "Tests failed. Not deploying."
fi

docker stop breeze-container
docker rm breeze-container
docker rmi breeze-image
rm -rf build
rm -rf dump
