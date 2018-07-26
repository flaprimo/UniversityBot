FROM alpine:3.8

# install system dependencies
RUN apk update && apk add python3

# set python path and working directory
WORKDIR /opt/UniversityBot

# copy application and install requirements.txt dependencies
COPY . ./
RUN pip3 install -r requirements.txt

# set volume
VOLUME ["/opt/UniversityBot/logs", "opt/UniversityBot/cache"]

# run application
CMD ["/usr/bin/python3", "/opt/UniversityBot/universitybot/polibot.py"]