#!/bin/bash -ex

# install-windows-stuff.ps1 should install Ubuntu

# Redeploying Ubuntu on WSL2:
# wsl2 --unregister Ubuntu
# wsl2 --install Ubuntu

# Run with:
# wget -O- https://bitbucket.org/dbesen/random/raw/master/redeploy.sh | bash

wait_for_keypress () {
    read -n 1 -s -r -p "Press any key to continue";echo
}

# The first sudo will ask for password.

sudo chsh -s $(which zsh) $(whoami)
sudo apt-get update
sudo apt-get install -y zsh zsh-doc git vim make python-pip dos2unix curl inotify-tools
sudo pip3 install requests

mkdir ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ''

clear
echo
echo MANUAL: Go to bitbucket.org, add public key to ssh keys:
echo
cat ~/.ssh/id_rsa.pub
echo
wait_for_keypress

mkdir bitbucket
cd bitbucket
git clone git@bitbucket.org:/dbesen/all_repos.git
./all_repos/update-all.sh

cd ~/bitbucket/settings
./install.sh

vim '+exit' # install vim plugins

exec zsh
