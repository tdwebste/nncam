#!/bin/bash
gcc -Wl,-rpath -Wl,'$ORIGIN' -L. -g -o demoraw{,.cpp} -lnncam -I
