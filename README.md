# UniversityBot
<a href='https://travis-ci.org/flaprimo/UniversityBot'><img src='https://secure.travis-ci.org/flaprimo/UniversityBot.png?branch=master'></a>

UnivesityBot is the bot that ease your life at Politecnico di Milano.
Use it to find information about halls, free classrooms and useful links.

## Features
### Available commands
* shows useful links
* gets classroom information (building, photo, notes, directions)
* searches for free classrooms

### Technologies
* file cache requests for api calls for faster response
* deployment using [docker](https://www.docker.com/)
* multi-language support through the [gettext](https://www.gnu.org/software/gettext/) standard
* use of the tested and reliable [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) framework

## Credits
* Flavio Primo ([@flaprimo](https://github.com/flaprimo/))
* Paolo Paterna ([@TopoDiFogna](https://github.com/TopoDiFogna))

## Installation instructions

1. [Install Docker](https://docs.docker.com/engine/installation/) CE edition (including [post-installation](https://docs.docker.com/engine/installation/linux/linux-postinstall/) instructions)
2. clone this repository in /opt/ or wherever you want
3. If you cloned in /opt/ just run `docker_install.sh` and **you're done** (if you stop the container just run `docker_run.sh` to restart it), else continue reading
4. open a terminal into project folder and build the docker image with `docker build -t universitybot .`
5. run the docker image with:
    `docker run --name=universitybot -v installdir/logs:/opt/UniversityBot/logs -v installdir/cache:/opt/UniversityBot/cache -v installdir/config:/opt/UniversityBot/config --restart=on-failure:10 universitybot`

## TODO
- [ ] implement inline
- [ ] implement add arguments to commands
- [ ] implement occupation, returns html of the occupation of the day
- [ ] implement room occupation, returns classroom occupation based on the day, https://github.com/jarrekk/imgkit
- [ ] webhook
- [ ] run docker image on travis
- [ ] add more translations (Spanish, German, Dutch, Arabic, Portuguese and Korean)