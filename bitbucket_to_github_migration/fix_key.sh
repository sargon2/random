#!/usr/bin/bash -ex

sudo mkdir -m 0755 -p /etc/apt/keyrings/

wget -O- https://cli.github.com/packages/githubcli-archive-keyring.gpg |
    gpg --dearmor |
    sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
    sudo chmod 644 /etc/apt/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \

sudo chmod 644 /etc/apt/sources.list.d/github-cli.list

