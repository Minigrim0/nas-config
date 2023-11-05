mkdir -p .config/{jellyfin,radarr,sonarr,qbit,jackett,ha}
mkdir -p {.downloads,Movies,Series}

docker-compose up --build -d