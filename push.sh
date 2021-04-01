#!/bin/sh

git add .

now=`date`

message=$(date +'%m/%d/%Y')

git commit -m message

git push origin master

