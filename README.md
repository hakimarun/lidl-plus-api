# Lidl Plus API

Lokale Web-App, die die API der Lidl Plus Android-App dokumentiert und zum
Ausprobieren bereitstellt. Alle Aufrufe laufen über einen kleinen lokalen Proxy,
die Anmeldung erfolgt per OAuth2 mit PKCE gegen das eigene Lidl-Konto.

Die API-Beschreibung wurde statisch aus der App rekonstruiert. Kein offizielles
Projekt, nicht mit Lidl verbunden. Gedacht für den persönlichen Zugriff auf die
eigenen Daten und für Lern- und Forschungszwecke. Es werden ausschließlich die
eigenen Kontodaten abgerufen.

## Funktionen

- Übersicht aller gefundenen Endpunkte, nach Modul gruppiert, mit Suche
- Jeder Endpunkt direkt ausprobierbar, Antwort wird formatiert angezeigt
- Anmeldung per OAuth2 PKCE, inklusive optionalem URL-Handler, der die
  Weiterleitung automatisch abfängt
- Felder wie Land, Sprache, Filiale, Bon, Pfand, Coupon oder Partner-Kampagne
  erscheinen als Dropdown, das vorher die passende Liste aus dem Konto lädt
- Proxy entpackt gzip, deflate, brotli und zstd

## Einrichtung

Voraussetzung ist Python 3.

Der Token-Endpunkt verlangt eine Client-Authentifizierung. Der dafür nötige Wert
steht bewusst nicht im Repo. Hinterlege ihn lokal über eine Umgebungsvariable
oder eine nicht versionierte Datei:

```bash
export LIDL_CLIENT_SECRET="..."
# oder
echo "..." > webapp/client_secret.txt
```

## Start

```bash
cd webapp
python3 server.py
```

Dann `http://127.0.0.1:8777` im Browser öffnen. Der Server bindet nur an
127.0.0.1.

## Anmelden

1. In der App auf Anmelden, dann Login öffnen.
2. Im Browser einloggen. Nach dem Login leitet Lidl auf das App-Schema
   `com.lidlplus.app://` weiter, das der Browser nicht öffnen kann.
3. Entweder den Code aus der Weiterleitung einfügen, oder den optionalen
   URL-Handler installieren, der die Weiterleitung automatisch abfängt:

```bash
bash webapp/url-handler/install.sh
```

Entfernen mit `bash webapp/url-handler/uninstall.sh`.

Die Tokens werden lokal in `webapp/tokens.json` abgelegt. Diese Datei steht in
`.gitignore` und darf nicht geteilt werden.

## Dateien

- `webapp/server.py` lokaler Server und Proxy, nur Standardbibliothek
- `webapp/index.html` die Oberfläche
- `webapp/endpoints.json` die Endpunkt-Daten
- `webapp/url-handler/` optionaler Handler für das App-Schema
- `lidl_auth.py` dasselbe als Kommandozeilen-Werkzeug
- `LIDL_PLUS_API.md` und `lidl_plus_api.json` die rekonstruierte API-Doku
