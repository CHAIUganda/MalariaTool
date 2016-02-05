#!/usr/bin/env bash
ansible-playbook db_server.yml -i inventory/hosts.ini -vvvv
