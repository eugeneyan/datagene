#!/usr/bin/env bash
uwsgi --socket 127.0.0.1:6688 --ini uwsgi.ini >> web.log 2>&1

mail -s "[ALERT] datagene.io down" eugeneyanziyou@gmail.com </dev/null