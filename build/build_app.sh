cd app
docker build -t app:latest -f Dockerfile .
cd ..
echo "'app' image built --> app:latest"