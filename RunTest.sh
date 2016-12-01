#!/bin/bash
ansible-playbook checkNet.yml -i hosts --extra-vars "inventory=checkNet-matrix.yml"
