#!/usr/bin/bash -ex

mkdir -p ~/.config/systemd/user/

cp dropbox.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable dropbox
systemctl --user start dropbox

loginctl enable-linger $USER
