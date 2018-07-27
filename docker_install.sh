#!/bin/bash

git pull
docker build -t universitybot .
docker run -d --name=universitybot -v /opt/UniversityBot/logs:/opt/UniversityBot/logs -v /opt/UniversityBot/cache:/opt/UniversityBot/cache -v /opt/UniversityBot/config:/opt/UniversityBot/config --restart=on-failure:10 universitybot