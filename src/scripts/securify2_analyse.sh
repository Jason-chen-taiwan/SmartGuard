#!/bin/bash
#securify只能處理0.5.0以上的版本
#Token.sol
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <filename> <solc-version>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
sudo docker run --rm -e SOLC_VERSION=$2 -v "$PWD":/share securify2 /share/$filename $3 > result

