#!/bin/sh
export PYTHONPATH=$PYTHONPATH:src/main
echo $PYTHONPATH
python3 -m unittest discover -v -s 'src/tests'
