#!/bin/bash

# example在/home/sixsquare/smart_contract_analyse/json_analyse: sudo bash ../generate_AST.sh ../ast_json/educoin.sol 0.4.25
# 检查是否有两个参数传递给脚本
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: $0 <file-path> [version]"
    exit 1
fi

# 获取文件的绝对路径
file_path=$(realpath "$1")

# 获取文件名
file_name=$(basename "$file_path")

# 设置默认版本
if [ $# -eq 1 ]; then
    version="latest"
else
    version=$2
fi

# 检查文件是否存在
if [ ! -f "$file_path" ]; then
    echo "Error: File does not exist."
    exit 1
fi

# 检查文件是否已在当前目录
if [ -f "$file_name" ]; then
    echo "File is already in the current directory."
else
    # 复制文件到当前目录
    cp "$file_path" .
    # echo "File has been copied to the current directory."
fi

# docker run --rm -v $(pwd):/sources ethereum/solc:$version --ast-compact-json /sources/$file_name > Solidity_AST.json
docker run --rm -v $(pwd):/sources ethereum/solc:$version --ast-compact-json /sources/$file_name > Solidity_AST.json 2> /dev/null

sed '1,4d' Solidity_AST.json > temp_file
mv temp_file Solidity_AST.json
./json_analyse ./Solidity_AST.json $file_name
rm Solidity_AST.json
rm $file_name
exit 0
