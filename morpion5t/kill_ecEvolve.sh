#!/bin/bash

#PIDS=$(ps -ef| grep ec.Evolve | grep -v grep |awk '{print $2}')

#echo $PIDS

#kill $PIDS

ps -U hashan | egrep -v "ssh|screen" | cut -b11-15 | xargs -t kill