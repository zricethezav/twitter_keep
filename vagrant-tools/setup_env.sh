#!/usr/bin/env bash

# TODO generalize the nice grepness into a function

sudo apt-get install -y python-pip
pip install virtualenv virtualenvwrapper

mkdir -p /home/vagrant/.virtualenvs

export WORKON_HOME=/home/vagrant/.virtualenvs
source_line="export WORKON_HOME=~/.virtualenv"
grep -q "^${source_line}" /home/vagrant/.bashrc || \
    echo "${source_line}" >> /home/vagrant/.bashrc

. /usr/local/bin/virtualenvwrapper.sh
source_line=". /usr/local/bin/virtualenvwrapper.sh"
grep -q "^${source_line}" /home/vagrant/.bashrc || \
    echo "${source_line}" >> /home/vagrant/.bashrc

