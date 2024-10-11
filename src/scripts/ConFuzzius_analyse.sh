#!/bin/bash
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <filename> <solc-version> [additional-args]"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
additional_args=${3:-""}

if [ -z "$additional_args" ]; then
    sudo docker run --rm -v "$PWD":/share confuzzius bash -c "\
    python3 fuzzer/main.py -s /share/$filename --solc v$solc_version --evm byzantium -g 20 2>&1 | tee /share/result \
    "
else
    sudo docker run --rm -v "$PWD":/share confuzzius bash -c "\
    python3 fuzzer/main.py -s /share/$filename --solc v$solc_version $additional_args 2>&1 | tee /share/result \
    "
fi
