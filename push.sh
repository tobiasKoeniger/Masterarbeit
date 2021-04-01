#!/bin/sh

git add .

now=`date`

message=$(date +'%m/%d/%Y')

echo message

git commit -m message

git push origin master

