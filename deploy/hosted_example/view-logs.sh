#!/bin/bash

tail -f $(docker volume inspect tt-logs | jq -r '.[0].Mountpoint')/publisher.log

