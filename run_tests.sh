#!/bin/sh
export PYTHONPATH=$PYTHONPATH:src/main
echo $PYTHONPATH
python3 -m unittest discover -s 'src/tests'
