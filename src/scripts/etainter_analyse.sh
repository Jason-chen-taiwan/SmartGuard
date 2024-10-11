#!/bin/bash

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <filename> <solc-version> [additional-args]"
    exit 1
fi

filename=$(basename "$1")
solc_version=$2
additional_args=${3:-""}  # 如果第三個參數不存在，則使用空字符串

# 構建 docker 命令
if [ -z "$additional_args" ]; then
    docker_command="python bin/analyzer.py -f /share/$filename -b -m 8 2>&1 | tee /share/result"
else
    docker_command="python bin/analyzer.py -f /share/$filename $additional_args 2>&1 | tee /share/result"
fi

# 執行 docker 命令並捕獲錯誤信息
sudo docker run --rm -v "$PWD":/share etainter bash -c "$docker_command" || {
    echo "Docker command failed"
    exit 1
}

exit 0
