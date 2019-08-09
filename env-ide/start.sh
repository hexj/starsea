docker-compose up
docker logs starsea 2>&1 | grep "token" | grep -v "NotebookApp"