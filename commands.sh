# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target

# [Service]
# User=ubuntu
# Group=www-data
# WorkingDirectory=/home/ubuntu/projectattend/AttendanceYovi
# ExecStart=/home/ubuntu/projectattend/env/bin/gunicorn \
#           --access-logfile - \
#           --workers 3 \
#           --bind unix:/run/gunicorn.sock \
#           attendance.wsgi:application

# [Install]
# WantedBy=multi-user.target