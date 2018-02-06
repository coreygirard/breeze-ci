REPO="https://github.com/coreygirard/breeze-ci-example/archive/master.zip"

rm -rf build

mkdir build
mkdir build/shared

curl "$REPO" -L -o build/latest.zip
unzip build/latest.zip -d build/
mv build/breeze-ci-example-master build/latest

read -d $'\x04' TEST_PATH < "./build/latest/breeze.yml"
echo "Executing tests from: $TEST_PATH"

docker rm breeze-container
docker rmi breeze-image

docker build -t breeze-image -f "./Dockerfile" --no-cache --build-arg test_path="$TEST_PATH" ./
#docker run --name breeze-container breeze-image
docker run --name breeze-container --rm -i -t breeze-image

#docker start breeze-container
#docker attach breeze-container
#docker exec breeze-container ls
#mkdir reports
#touch reports/temp.txt
#ls ./reports
#docker exec breeze-container bash
#ls build/latest/example
#coverage run build/latest/example/test_example.py

#docker exec breeze-container touch temp.txt
#docker exec breeze-container ls

#docker build --no-cache -t --build-arg test_path="$TEST_PATH" breeze-latest .
#docker run -v "$PWD/build/shared:/shared" breeze-latest

TEST_RESULT=$?
echo "Received: $TEST_RESULT"
if [ $TEST_RESULT -eq "0" ]; then
  echo "Tests passed. Deploying..."
else
  echo "Tests failed. Not deploying."
fi

#rm -rf build
