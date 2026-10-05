#!/bin/bash
# Entfernt den URL Handler und hebt die Registrierung des Schemas auf.
set -e
cd "$(dirname "$0")"
APP="LidlPlusCatcher.app"
DEST="$HOME/Applications/$APP"
LSREG=/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister

[ -d "$DEST" ] && "$LSREG" -u "$DEST" || true
rm -rf "$DEST" "$APP"
echo "Entfernt. Das Schema com.lidlplus.app ist nicht mehr registriert."
