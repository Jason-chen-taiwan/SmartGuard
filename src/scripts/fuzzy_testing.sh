#!/bin/bash
filename=$(basename "$1")
version="$2"
additional_args="$3"

# echidna.sol
docker run --label app=echidna -v "$PWD":/home trailofbits/echidna bash -c "\
cd /home; \
touch result; \
solc-select install $version; \
solc-select use $version; \
if [ -z \"$additional_args\" ]; then \
    echidna-test ./$filename --test-mode assertion > result; \
else \
    echidna-test ./$filename $additional_args > result; \
fi"
docker rm $(docker ps -a -q --filter "label=app=echidna")

input_file="result"
output_file="output.txt"

awk '
BEGIN {buffer = ""} 
/^\[/ {buffer = ""} 
{buffer = buffer $0 "\n"} 
END {print buffer}' $input_file > $output_file

awk 'NR==1 {next} {lines[NR]=$0} END {for (i=2; i<=NR-6; i++) print lines[i]}' $output_file > $input_file

rm $output_file
rm -r crytic-export
exit 0