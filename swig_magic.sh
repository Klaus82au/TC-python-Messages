#!/bin/bash

swig -python load.i

python setup.py build_ext --inplace
