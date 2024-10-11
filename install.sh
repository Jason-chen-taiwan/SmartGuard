#!/bin/bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
sudo apt-get update
sudo apt  install cargo
if !command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed."
    echo "Installing Docker..."
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

#sudo docker pull trailofbits/eth-security-toolbox
    git clone https://github.com/crytic/slither.git
    sudo docker build -t trailofbits/eth-security-toolbox ./slither
    # sudo docker pull trailofbits/echidna
    docker pull trailofbits/echidna:v2.2.3
    #securify2 install
    sudo docker build -t securify2 ./securify2/
    #ConFuzzius install
    sudo docker build -t confuzzius ./ConFuzzius/
    #Ethainter install
    sudo docker build -t etainter ./eTainter_docker/
    #mythril install
    sudo docker build -t mythril ./mythril/
exit 0