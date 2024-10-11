#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename> <solc-version>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2

cp "../save_file/$filename" "./testing_file.sol"

docker run --label app=slither -v "$PWD":/share trailofbits/eth-security-toolbox bash -c "\
cd /share; \
solc-select install $solc_version; \
solc-select use $solc_version; \
slither ./testing_file.sol"

rm "./testing_file.sol"

docker rm $(docker ps -a -q --filter "label=app=slither")
exit 0