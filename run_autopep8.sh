#!/bin/sh


#autopep8 --ignore=W602,E501,E301,E309 -i *.py

source ~/.bash_profile
p2
yapf --style "pep8" -i *.py
