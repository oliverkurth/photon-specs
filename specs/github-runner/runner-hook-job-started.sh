#!/bin/sh

UID_GID="$(id -u):$(id -g)"
sudo find "${GITHUB_WORKSPACE}" -user root -exec chown "${UID_GID}" {} \;
