#!/bin/bash

# usage:
#
# to output an large optimized gif 10 fps 
# >   bash gifbatch.sh /home/zeffii/Videos/braindead/
#
# to output an --color 256 optimized gif 10 fps 
# >   bash gifbatch.sh /home/zeffii/Videos/braindead/ 256
#
# to output an --color 256 optimized gif 24 fps 
# >   bash gifbatch.sh /home/zeffii/Videos/braindead/ 256 24


if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    exit
fi

if [ $# -gt 0 ]; then
    mypath=$1
fi

pushd $mypath
pwd

if [ $# -eq 1 ]; then
    convert -delay 10 -loop 0 *png animated.gif &&
    gifsicle -O animated.gif > opt_animated.gif

fi

if [ $# -eq 2 ]; then
    colors=$2
    convert -delay 10 -loop 0 *png animated.gif &&
    gifsicle -O --colors $colors animated.gif > "opt_${colors}_animated.gif"

fi

if [ $# -eq 3 ]; then
    colors=$2
    framerate=$3
    convert -delay $framerate -loop 0 *png animated.gif &&
    gifsicle -O --colors $colors animated.gif > "opt_${colors}_animated_${framerate}fps.gif"
fi

popd
exit
