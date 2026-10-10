#!/bin/bash
set -e

export -p > /etc/cron.env

python -m app.cli update-rates || echo "Первичная загрузка курсов не удалась, cron повторит по расписанию"

crontab /code/docker/crontab
exec cron -f
