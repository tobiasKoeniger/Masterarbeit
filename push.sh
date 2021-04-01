#!/bin/sh

git add .

message=$(date +'%d/%m/%Y %H:%M')

echo "${message}"

git commit -m "${message}"

git push origin master

