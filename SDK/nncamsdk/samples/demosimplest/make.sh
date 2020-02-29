#!/bin/bash
gcc -Wl,-rpath -Wl,'$ORIGIN' -L. -g -o demosimplest{,.cpp} -lnncam
