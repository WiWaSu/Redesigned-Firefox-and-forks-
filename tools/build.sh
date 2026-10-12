#!/bin/sh
# Собирает архив установщика: FloorpModern-Setup-v<версия>.zip
# Проверяет, что версия в VERSION совпадает с версией в installer.ps1.
set -e
cd "$(dirname "$0")/.."
V=$(tr -d ' \r\n' < VERSION)
grep -q "\$Version = \"$V\"" files/installer.ps1 || { echo "Версия в installer.ps1 не совпадает с VERSION ($V)"; exit 1; }
OUT=${1:-.}/FloorpModern-Setup-v$V.zip
git archive --format=zip --prefix=FloorpModern-v$V/ -o "$OUT" HEAD
echo "$OUT"
