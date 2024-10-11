#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <filename> <solc-version>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
args = $3
# cp "./$filename" "./testing_file.sol"

docker run --label app=slither -v "$PWD":/share trailofbits/eth-security-toolbox bash -c "\
cd /share; \
solc-select install $solc_version; \
solc-select use $solc_version; \
slither $filename $args"

docker rm $(docker ps -a -q --filter "label=app=slither")
exit 0