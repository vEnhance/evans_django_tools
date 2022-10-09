#!/bin/bash

GOOD_FILE="/tmp/${PWD##*/}.good"
git rev-parse HEAD >"$GOOD_FILE"

echo -e "-----------------------------------------------------------------------"
echo -e "\033[1;31m$(git rev-parse HEAD)\033[0m had lint.sh bypassed"
echo -e "-----------------------------------------------------------------------"
