#!/bin/bash -ex

# This one is for termux only.  It sets up git but not Dropbox.

pkg install -y zsh git vim make dos2unix curl inotify-tools gnupg gh wget man less

chsh -s zsh

if [ ! -f ~/.ssh/id_ed25519 ]; then
    mkdir -p ~/.ssh
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ''
fi

gh auth login -p ssh -w --skip-ssh-key -s admin:public_key
gh ssh-key add ~/.ssh/id_ed25519.pub

mkdir -p ~/github
mkdir -p ~/github/sargon2

cd ~/github/sargon2
git clone git@github.com:sargon2/all_repos
cd ..

./sargon2/all_repos/update-all.sh

pushd sargon2/random
# This script was probably cloned over https, so reset the remote to use ssh
git remote set-url origin git@github.com:sargon2/random
popd

pushd sargon2/settings
./install.sh
popd

vim '+exit' # install vim plugins

exec zsh
