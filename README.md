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
Install `sudo apt install libssl-dev libcurl4-openssl-dev python-dev` if you want to use `pycurl` backend to make calls instead of `requests`.