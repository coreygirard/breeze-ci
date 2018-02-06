REPO="https://github.com/coreygirard/breeze-ci-example/archive/master.zip"

rm -rf build

mkdir build
#mkdir build/shared

curl "$REPO" -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest

read -d $'\x04' TEST_PATH < "./build/latest/breeze.yml"
echo "Executing tests from: $TEST_PATH"

docker rm breeze-container
docker rmi breeze-image

docker build -t breeze-image -f "./Dockerfile" --no-cache --build-arg test_path="$TEST_PATH" ./
docker run --name breeze-container --rm -i -t breeze-image

TEST_RESULT=$?
echo "Received: $TEST_RESULT"
if [ $TEST_RESULT -eq "0" ]; then
  echo "Tests passed. Deploying..."
else
  echo "Tests failed. Not deploying."
fi

cd build/latest
python setup.py sdist bdist_wheel
cd ../..
#rm -rf build
