#!/usr/bin/env bash


#msginit --locale=it --output=it/LC_MESSAGES/messages.po --input=messages.pot
#msgmerge --update --no-fuzzy-matching --backup=off it/LC_MESSAGES/messages.po messages.pot
msgfmt it/LC_MESSAGES/it.po --output-file it/LC_MESSAGES/it.mo