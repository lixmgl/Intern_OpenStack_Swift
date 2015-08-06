#!/bin/bash

cd /opt/graphite/webapp/graphite
python manage.py syncdb

chown -R www-data:www-data /opt/graphite/storage/

a2ensite graphite
