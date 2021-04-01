#!/bin/sh

git add .

message=$(date +'%m/%d/%Y')

echo "${message}"

git commit -m ${message}

git push origin master

