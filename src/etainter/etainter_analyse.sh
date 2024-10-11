#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename> <solc-version>"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2

# 檢查文件是否存在
if [ ! -f "../save_file/$filename" ]; then
    echo "File ../save_file/$filename does not exist"
    exit 1
fi

cp "../save_file/$filename" "./testing_file.code"

# 執行 docker 命令並捕獲錯誤信息
sudo docker run --rm -v "$PWD":/share etainter bash -c "\
python bin/analyzer.py -f /share/testing_file.code -b -m 8 -tt all 2>&1 | tee /share/result \
" || {
    echo "Docker command failed"
    exit 1
}

exit 0
