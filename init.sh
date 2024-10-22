#!/bin/bash

mkdir -p .config/{jellyfin,radarr,sonarr,qbit,jackett,ha}
mkdir -p ./{Movies,Series,.downloads}

docker compose up --build -d
