#!/bin/bash
if [ ! -n "$1" ]
then
    echo "Usages: sh iHealth_crawler.sh [start|stop|restart|status|log]"
    exit 0
fi

if [ $1 = start ]
then
    psid=`ps aux | grep "python" | grep "iHealth_crawler.py" | grep -v "grep" | wc -l`
    if [ $psid -gt 0 ]
    then
        echo "iHealth_crawler is running!"
        exit 0
    else
        nohup python iHealth_crawler.py > iHealth_crawler.log 2>&1 &
        echo "Start iHealth_crawler service [OK]"
    fi

elif [ $1 = stop ];then
    ps -ef | grep "iHealth_crawler.py" | grep -v grep | cut -c 10-15 | xargs kill -9
    echo "Stop iHealth_crawler service [OK]"

elif [ $1 = restart ];then
    ps -ef | grep "iHealth_crawler.py" | grep -v grep | cut -c 10-15 | xargs kill -9
    echo "Stop iHealth_crawler service [OK]"
    sleep 2
    nohup python iHealth_crawler.py > iHealth_crawler.log 2>&1 &
    echo "Start iHealth_crawler service [OK]"

elif [ $1 = status ];then
    ps -ef | grep "iHealth_crawler.py" | grep -v grep

elif [ $1 = log ];then
    tail -f iHealth_crawler.log

else
    echo "Usages: sh server.sh [start|stop|restart|status|log]"
fi
