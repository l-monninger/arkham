#!/bin/bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 801781668887.dkr.ecr.us-west-2.amazonaws.com
docker build -t arkham-blocks .
docker tag arkham-blocks 801781668887.dkr.ecr.us-west-2.amazonaws.com/arkham-blocks:latest
docker push 801781668887.dkr.ecr.us-west-2.amazonaws.com/arkham-blocks:latest

aws lightsail push-container-image --region us-west-2 --service-name container-service-1 --label container-service-1a --image arkham-blocks:latest