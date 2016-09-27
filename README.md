# wp-labora-py
Python stuff for sync with labora

## Example import_config.cfg file

```
[config]
ics_url=<URL TO iCal download>
ics_filename=events.ics
wp_user=admin
wp_pwd=<Password for WP user>
wp_url=http://localhost:80
event_category=<WordPress category>
dry_run=<1 | 0>
```

### External libs
Dependent on - curl, python-dateutil, pytz, iCalendar and python-wordpress-xmlrpc
```
The curl package - apt-get install curl
<https://python-wordpress-xmlrpc.readthedocs.org/>
<https://github.com/maxcutler/python-wordpress-xmlrpc.git/>
<https://github.com/collective/icalendar/>
pip install pytz - or - apt-get install python-pytz
pip install logging
apt-get install python-pip
apt-get install python-dateutil
```

