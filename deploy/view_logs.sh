#!/bin/bash

tail -f $(podman volume inspect tt-logs | jq -r '.[0].Mountpoint')/publisher.log
