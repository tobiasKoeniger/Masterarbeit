#!/bin/sh

git add .

now=`date`

message=$(now +'%m/%d/%Y')

echo message

git commit -m message

git push origin master

