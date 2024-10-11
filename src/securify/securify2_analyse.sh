#!/bin/bash
#securify只能處理0.5.0以上的版本

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename> <solc-version>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
cp "../save_file/$filename" "./testing_file.sol"
sudo docker run --rm -e SOLC_VERSION=$2 -v "$PWD":/share securify2 /share/testing_file.sol > result

rm "./testing_file.sol"
