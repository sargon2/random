#!/bin/bash -ex

# install-windows-stuff.ps1 should install Ubuntu

# Redeploying Ubuntu on WSL2:
# wsl --unregister Ubuntu
# wsl --install Ubuntu

# Run with:
# bash -ex <(wget -o /dev/null -O- https://bitbucket.org/dbesen/random/raw/master/redeploy.sh)

wait_for_keypress () {
    read -n 1 -s -r -p "Press any key to continue";echo
}

# The first sudo will ask for password.

sudo apt-get update
sudo apt-get install -y zsh zsh-doc git vim make python3-pip dos2unix curl inotify-tools gnupg
sudo pip3 install requests

sudo chsh -s $(which zsh) $(whoami)

mkdir ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ''

clear
echo
echo MANUAL: Go to bitbucket.org, add public key to ssh keys:
echo
cat ~/.ssh/id_ed25519.pub
echo
wait_for_keypress

mkdir bitbucket
cd bitbucket
git clone git@bitbucket.org:/dbesen/all_repos.git
./all_repos/update-all.sh

cd ~/bitbucket/settings
./install.sh

vim '+exit' # install vim plugins

clear
echo
echo MANUAL: Visit the link to log in to dropbox after it appears.
echo
wait_for_keypress

cd ~/bitbucket/random
./reinstall-dropbox.sh

cp -R ~/Dropbox/aws/.aws ~

# GPG
gpg --batch --import ~/Dropbox/gpg/private_key.txt

# Extract the key ID of the imported key
KEY_ID=$(gpg --list-keys --with-colons --fingerprint | awk -F: '/^fpr:/ {print $10; exit}')

# Set the trust level to ultimate for the imported key
echo "$KEY_ID:6:" | gpg --batch --import-ownertrust

exec zsh
