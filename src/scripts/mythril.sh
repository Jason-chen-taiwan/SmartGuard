#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <filename> <solc-version> <args>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
args=$3

# Run the Mythril Docker container to analyze the smart contract
docker run --label app=mythril -v "$PWD":/share --entrypoint /bin/bash mythril -c "\
cd /share
myth analyze $args $filename >> result"

# Remove the container after use
docker rm $(docker ps -a -q --filter "label=app=mythril")


exit 0
