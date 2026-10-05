#!/bin/bash
# Baut den URL Handler und registriert das Schema com.lidlplus.app fuer diesen
# Nutzer. Reversibel ueber uninstall.sh.
set -e
cd "$(dirname "$0")"
APP="LidlPlusCatcher.app"
PLB=/usr/libexec/PlistBuddy
LSREG=/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister

rm -rf "$APP"
osacompile -o "$APP" handler.applescript
PLIST="$APP/Contents/Info.plist"

$PLB -c "Add :CFBundleIdentifier string com.local.lidlpluscatcher" "$PLIST" 2>/dev/null \
  || $PLB -c "Set :CFBundleIdentifier com.local.lidlpluscatcher" "$PLIST"
$PLB -c "Add :LSUIElement bool true" "$PLIST" 2>/dev/null \
  || $PLB -c "Set :LSUIElement true" "$PLIST"
$PLB -c "Add :CFBundleURLTypes array" "$PLIST" 2>/dev/null || true
$PLB -c "Add :CFBundleURLTypes:0 dict" "$PLIST" 2>/dev/null || true
$PLB -c "Add :CFBundleURLTypes:0:CFBundleURLName string com.lidlplus.app" "$PLIST" 2>/dev/null \
  || $PLB -c "Set :CFBundleURLTypes:0:CFBundleURLName com.lidlplus.app" "$PLIST"
$PLB -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes array" "$PLIST" 2>/dev/null || true
$PLB -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string com.lidlplus.app" "$PLIST" 2>/dev/null \
  || $PLB -c "Set :CFBundleURLTypes:0:CFBundleURLSchemes:0 com.lidlplus.app" "$PLIST"

# an einen festen Ort legen, damit der Pfad stabil bleibt
DEST="$HOME/Applications"
mkdir -p "$DEST"
rm -rf "$DEST/$APP"
cp -R "$APP" "$DEST/$APP"
touch "$DEST/$APP"

"$LSREG" -f "$DEST/$APP"
echo "Installiert nach $DEST/$APP und registriert fuer com.lidlplus.app"
echo "Test: open 'com.lidlplus.app://callback?code=TESTCODE'"
