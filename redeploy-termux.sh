#!/bin/bash -ex

# This one is for termux only.  It sets up git but not Dropbox.

pkg install -y zsh zsh-doc git vim make dos2unix curl inotify-tools gnupg gh wget

chsh -s zsh

mkdir ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ''

gh auth login -p ssh -w --skip-ssh-key
gh ssh-key add ~/.ssh/id_ed25519.pub

mkdir -p ~/github
mkdir -p ~/github/sargon2
cd ~/github/sargon2
git clone github.com/sargon/all_repos
./all_repos/update-all.sh

cd settings
./install.sh

vim '+exit' # install vim plugins

exec zsh
