#!/bin/bash

# installing the postgres
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql.service
