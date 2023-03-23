#!/bin/bash
docker build --platform=linux/amd64 -t arkham-blocks .
docker tag arkham-blocks gcr.io/useful-hour-357005/arkham-blocks
docker push gcr.io/useful-hour-357005/arkham-blocks