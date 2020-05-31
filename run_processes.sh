sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo:latest

sudo docker run -d -it --name app_python --mount type=bind,source="$(pwd)"