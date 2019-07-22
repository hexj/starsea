docker-compose up -d
sleep 3
docker logs starsea 2>&1 | grep "token" | grep -v "NotebookApp"