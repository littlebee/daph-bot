#!/usr/bin/env bash

HOST=pi@trainerbot.local

# add your rsa public key to authorized keys so we
# don't need to enter a password
cat ~/.ssh/id_rsa.pub | ssh $HOST "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
ssh $HOST 'mkdir -p ~/data && mkdir -p ~/logs'
