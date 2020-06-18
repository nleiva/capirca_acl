#!/bin/bash

# https://unix.stackexchange.com/questions/285924/how-to-compare-a-programs-version-in-a-shell-script/285928#285928

current=$(grep 'version:' galaxy.yml | cut -d' ' -f2)
new=$TAG

 if [ "$(printf '%s\n' "$new" "$current" | sort -V | head -n1)" = "$new" ]; then 
        echo "New version ${new} isn't valid (is less or equal than ${current})"
 else
        echo "New version ${new} is valid (is greater than ${current})"
 fi