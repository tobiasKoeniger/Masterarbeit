#!/bin/sh

# git script

cd ~/Software/

git config --global user.email "tobias.koeniger@googlemail.com"

git add .

message=$(date +'%d/%m/%Y %H:%M')

echo "${message}"

git commit -m "${message}"

git push origin master


