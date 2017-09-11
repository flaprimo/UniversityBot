#!/usr/bin/env bash
# to create and update translation please use poedit

xgettext --files-from=POTFILES.in --directory=.. --output=messages.pot --copyright-holder="Flavio Primo" --package-name="UNIVERSITY BOT" --package-version="1.0" --msgid-bugs-address="project's issue github page"