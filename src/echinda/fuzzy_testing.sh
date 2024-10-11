#!/bin/bash
filename=$(basename "$1")
cp ../save_file/$filename ./testing_file.sol
docker run --label app=echinda -v "$PWD":/home trailofbits/echidna bash -c "\
cd /home; \
touch result; \ 
solc-select install $2; \
solc-select use $2; \
echidna-test ./testing_file.sol --test-mode assertion> result;"
rm testing_file.sol
docker rm $(docker ps -a -q --filter "label=app=echinda")

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