cd worker
docker build -t worker:latest -f Dockerfile .
cd ..
echo "'worker' image built --> worker:latest"