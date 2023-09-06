#!/bin/sh
#
#   zenity:  see also https://help.gnome.org/users/zenity/stable/
#

FILE=`zenity --file-selection --title="Select an athinput" --filename=athinput.linear_wave1d`

if [  $? = 0 ]; then
    echo $FILE
elif [ $? -gt 0 ]; then
    echo Cancel
else
    echo Bad too
fi
