#!/usr/bin/env sh
export ANSIBLE_HOST_KEY_CHECKING=False

PROVISIONING_FOLDER=./provisioning
ANSIBLE_BIN_NAME=ansible-playbook
ANSIBLE_BIN=$(command -v $ANSIBLE_BIN_NAME 2>/dev/null)

if [ -z "$ANSIBLE_BIN" ]; then
	echo "$ANSIBLE_BIN_NAME was not found on this system"
	exit 1
fi

## Vagrant Deploy

cd $PROVISIONING_FOLDER
$ANSIBLE_BIN -u vagrant -i local site.yml --private-key ../.vagrant/machines/honeypot/virtualbox/private_key 
