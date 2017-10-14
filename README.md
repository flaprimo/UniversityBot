# UniversityBot
<a href='https://travis-ci.org/flaprimo/UniversityBot'><img src='https://secure.travis-ci.org/flaprimo/UniversityBot.png?branch=master'></a>

UnivesityBot is the bot that ease your life at Politecnico di Milano.
Use it to find information about halls, free classrooms and useful links.

## Features
* shows useful links
* shows free classrooms
* in memory cache requests for api calls for faster response
* multi-language support through the [gettext](https://www.gnu.org/software/gettext/) standard
* use of the tested and reliable [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) framework

## Credits
* Flavio Primo ([@flaprimo](https://github.com/flaprimo/))
* Paolo Paterna ([@TopoDiFogna](https://github.com/TopoDiFogna))

## Installation instructions
Install `sudo apt install libssl-dev libcurl4-openssl-dev python3-dev` if you want to use `pycurl` backend to make calls instead of `requests`.

1. [Install Docker](https://docs.docker.com/engine/installation/) CE edition (including [post-installation](https://docs.docker.com/engine/installation/linux/linux-postinstall/) instructions)
2. Install [Docker Compose](https://docs.docker.com/compose/install/#install-compose)
3. clone this repository
4. open a terminal into project folder and build the docker image with `docker build -t universitybot .`
5. run the docker image with:
    * on a development environment would probably be:
    `docker run --volume=/home/$USER/Workspace/UniversityBot:/opt/UniversityBot universitybot`
    * on a production environment would probably be:
    `docker run --name=universitybot --restart=on-failure:10 --volume=/home/$USER/UniversityBot/conf:/opt/UniversityBot/conf universitybot`