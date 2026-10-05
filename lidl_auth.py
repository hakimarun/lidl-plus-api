#!/usr/bin/env python3
"""
Lidl Plus - OAuth2 Authorization-Code-Flow mit PKCE (Produktion).

Meldet dich mit deinem EIGENEN Lidl-Plus-Konto an und holt ein Access-Token,
mit dem du die dokumentierten PROD-Endpunkte aufrufen kannst.

Rekonstruiert aus der Android-App 17.11.4:
  issuer        https://accounts.lidl.com/
  authorize     GET  /connect/authorize
  token         POST /connect/token
  client_id     LidlPlusNativeClient   (Public Client, kein Secret)
  scope         openid profile offline_access lpprofile lpapis
  redirect_uri  com.lidlplus.app://callback
  PKCE          S256

Ablauf (redirect_uri ist ein Custom-Scheme, daher halb-manuell):
  1) python3 lidl_auth.py login --country DE --lang de
     -> oeffnet/zeigt die Login-URL. Im Browser einloggen.
  2) Der Browser leitet am Ende auf  com.lidlplus.app://callback?code=...
     weiter (die Seite "laedt nicht" / zeigt Fehler - das ist normal).
     Diese komplette URL aus der Adresszeile kopieren und einfuegen.
  3) Skript tauscht den Code gegen Tokens, speichert sie in tokens.json.
  4) python3 lidl_auth.py call https://tickets.lidlplus.com/api/v3/DE/tickets?yearOffset=0
     ruft einen Endpunkt mit gueltigem Bearer-Token auf (auto-refresh).

Nur Standardbibliothek + requests.  pip install requests
"""
import argparse, base64, hashlib, json, os, secrets, sys, urllib.parse, webbrowser
import requests

ISSUER       = "https://accounts.lidl.com/"
CLIENT_ID    = "LidlPlusNativeClient"
# Secret steht nicht im Repo, aus Umgebungsvariable oder client_secret.txt lesen
CLIENT_SECRET = (os.environ.get("LIDL_CLIENT_SECRET") or "").strip()
if not CLIENT_SECRET:
    try: CLIENT_SECRET = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_secret.txt")).read().strip()
    except Exception: CLIENT_SECRET = ""
SCOPE        = "openid profile offline_access lpprofile lpapis"
REDIRECT_URI = "com.lidlplus.app://callback"
APP_VERSION  = "17.11.4"
TOKENS_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokens.json")

def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def pkce_pair():
    verifier  = b64url(secrets.token_bytes(64))               # 43-128 Zeichen
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge

def save(tok: dict):
    json.dump(tok, open(TOKENS_FILE, "w"), indent=2)
    print(f"[+] Tokens gespeichert: {TOKENS_FILE}")

def load() -> dict:
    if not os.path.exists(TOKENS_FILE):
        sys.exit("[!] Keine tokens.json - erst 'login' ausfuehren.")
    return json.load(open(TOKENS_FILE))

# ---------------------------------------------------------------- login
def cmd_login(args):
    verifier, challenge = pkce_pair()
    state = b64url(secrets.token_bytes(16))
    nonce = b64url(secrets.token_bytes(16))
    params = {
        "client_id":             CLIENT_ID,
        "response_type":         "code",
        "scope":                 SCOPE,
        "redirect_uri":          REDIRECT_URI,
        "code_challenge":        challenge,
        "code_challenge_method": "S256",
        "state":                 state,
        "nonce":                 nonce,
        # App-spezifische Zusatzparameter:
        "Country":               args.country,
        "language":              f"{args.lang}-{args.country}",
        "track":                 "false",
        "force":                 "false",
    }
    url = ISSUER + "connect/authorize?" + urllib.parse.urlencode(params)
    print("\n=== 1) Im Browser einloggen ===\n")
    print(url + "\n")
    if not args.no_browser:
        try: webbrowser.open(url)
        except Exception: pass
    print("=== 2) Nach dem Login landet der Browser auf")
    print(f"       {REDIRECT_URI}?code=...  (Seite laedt nicht - normal).")
    print("       Komplette URL aus der Adresszeile hier einfuegen:\n")
    redirected = input("callback-URL: ").strip()

    q = urllib.parse.parse_qs(urllib.parse.urlparse(redirected).query)
    if "error" in q:
        sys.exit(f"[!] Auth-Fehler: {q['error']} {q.get('error_description','')}")
    if "code" not in q:
        sys.exit("[!] Kein ?code= in der URL gefunden.")
    if q.get("state", [None])[0] != state:
        print("[!] Warnung: state stimmt nicht ueberein (CSRF-Check).")
    code = q["code"][0]

    r = requests.post(ISSUER + "connect/token", data={
        "grant_type":    "authorization_code",
        "client_id":     CLIENT_ID,
        "code":          code,
        "redirect_uri":  REDIRECT_URI,
        "code_verifier": verifier,
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}, auth=(CLIENT_ID, CLIENT_SECRET), timeout=30)
    if r.status_code != 200:
        sys.exit(f"[!] Token-Exchange fehlgeschlagen: {r.status_code}\n{r.text}")
    tok = r.json(); tok["_country"] = args.country; tok["_lang"] = args.lang
    save(tok)
    print(f"[+] access_token (gekuerzt): {tok['access_token'][:24]}...")
    print(f"[+] gueltig fuer {tok.get('expires_in','?')} s, scope: {tok.get('scope')}")

# ---------------------------------------------------------------- refresh
def cmd_refresh(args):
    tok = load()
    if "refresh_token" not in tok:
        sys.exit("[!] Kein refresh_token vorhanden.")
    r = requests.post(ISSUER + "connect/token", data={
        "grant_type":    "refresh_token",
        "client_id":     CLIENT_ID,
        "refresh_token": tok["refresh_token"],
    }, headers={"Content-Type": "application/x-www-form-urlencoded"}, auth=(CLIENT_ID, CLIENT_SECRET), timeout=30)
    if r.status_code != 200:
        sys.exit(f"[!] Refresh fehlgeschlagen: {r.status_code}\n{r.text}")
    new = r.json()
    tok.update(new)                       # refresh_token rotiert ggf.
    save(tok)
    print("[+] Token erneuert.")
    return tok

# ---------------------------------------------------------------- call
def cmd_call(args):
    tok = load()
    def do(t):
        h = {
            "Authorization":    f"Bearer {t['access_token']}",
            "App":              "com.lidl.eci.lidlplus",
            "App-Version":      APP_VERSION,
            "Operating-System": "Android",
            "Accept-Language":  f"{t.get('_lang','de')}-{t.get('_country','DE')}",
        }
        for kv in args.header:            # zusaetzliche -H "Name: Wert"
            k, _, v = kv.partition(":"); h[k.strip()] = v.strip()
        return requests.request(args.method, args.url, headers=h,
                                data=args.data, timeout=30)
    r = do(tok)
    if r.status_code == 401:              # abgelaufen -> einmal refreshen
        print("[*] 401 - versuche Refresh ...")
        tok = cmd_refresh(args); r = do(tok)
    print(f"HTTP {r.status_code}")
    ct = r.headers.get("content-type", "")
    if "json" in ct:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    else:
        print(r.text[:4000])

# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description="Lidl Plus OAuth2/PKCE (eigenes Konto, PROD)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("login", help="Login + Token holen")
    pl.add_argument("--country", default="DE", help="ISO-Land, z.B. DE")
    pl.add_argument("--lang",    default="de", help="Sprache, z.B. de")
    pl.add_argument("--no-browser", action="store_true", help="Browser nicht auto-oeffnen")
    pl.set_defaults(func=cmd_login)

    pr = sub.add_parser("refresh", help="Access-Token per refresh_token erneuern")
    pr.set_defaults(func=cmd_refresh)

    pc = sub.add_parser("call", help="Endpunkt mit Bearer-Token aufrufen")
    pc.add_argument("url")
    pc.add_argument("-X", "--method", default="GET")
    pc.add_argument("-H", "--header", action="append", default=[])
    pc.add_argument("-d", "--data", default=None)
    pc.set_defaults(func=cmd_call)

    args = p.parse_args(); args.func(args)

if __name__ == "__main__":
    main()
