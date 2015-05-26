#!/bin/bash

if ! pgrep -a java | grep logstash; then
    echo Running logstash -f syslog.conf
    sudo ./bin/logstash -f syslog.conf -l syslog.log &
    sleep 3s
    pgrep java -a | grep logstash | awk '{print $1}' > syslog.pid
else
    echo Another logstash is running
fi

