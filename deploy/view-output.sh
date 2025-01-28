#!/bin/bash

xdg-open $(podman volume inspect tt-debug | jq -r '.[0].Mountpoint')

