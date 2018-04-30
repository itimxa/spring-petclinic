#!/bin/sh

export APP_USER=application
export APP_PASS=megasecurepass
export DB_USER=application_user
export DB_PASS=secretpass123
export DB_NAME=petclinic
export DB_HOST=192.168.33.10
export DB_PORT=3306
#export

if [ -f .vagrant/machines/db_vm/virtualbox/id ]
then
  vagrant up --provision
else
  vagrant up
fi
