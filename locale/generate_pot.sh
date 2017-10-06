#!/usr/bin/env bash
# to create and update translation please use poedit

xgettext --files-from=POTFILES.in --directory=.. --output=messages.pot --copyright-holder="Flavio Primo, Paolo Paterna" --package-name="UNIVERSITY BOT" --package-version="1.0" --msgid-bugs-address="https://github.com/flaprimo/UniversityBot/issues"