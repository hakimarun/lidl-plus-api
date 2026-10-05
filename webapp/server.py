#!/usr/bin/env python3
"""
Lidl Plus API, lokaler Server.

Dient die Doku Seite aus und arbeitet als Proxy, damit Aufrufe gegen die
echten Endpunkte nicht an CORS scheitern. Authentifizierung laeuft ueber
OAuth2 mit PKCE gegen die Produktion mit deinem eigenen Konto.

Nur Standardbibliothek. Start:
    python3 server.py
Dann http://127.0.0.1:8777 oeffnen.

Bindet absichtlich nur an 127.0.0.1. Tokens liegen in tokens.json neben
dieser Datei im Klartext, nicht teilen oder committen.
"""
import base64, hashlib, http.server, json, os, re, secrets, socketserver, ssl
import time, urllib.parse, urllib.request, urllib.error

HERE        = os.path.dirname(os.path.abspath(__file__))
PORT        = int(os.environ.get("PORT", "8777"))
ISSUER      = "https://accounts.lidl.com/"
CLIENT_ID   = "LidlPlusNativeClient"
# Der Token Endpunkt verlangt eine Client Authentifizierung per HTTP Basic.
# Das Secret steht NICHT im Repo. Lokal aus Umgebungsvariable LIDL_CLIENT_SECRET
# oder aus der nicht versionierten Datei client_secret.txt neben dieser Datei.
def _load_secret():
    v = os.environ.get("LIDL_CLIENT_SECRET")
    if v: return v.strip()
    try: return open(os.path.join(HERE, "client_secret.txt")).read().strip()
    except Exception: return ""
CLIENT_SECRET = _load_secret()
SCOPE       = "openid profile offline_access lpprofile lpapis"
REDIRECT    = "com.lidlplus.app://callback"
APP_VERSION = "17.11.4"
TOKENS_FILE = os.path.join(HERE, "tokens.json")

STATE = {}            # letzter Start und last_catch, im Speicher
PENDING = {}          # state -> {verifier, country, lang, at}, je Login eigener Eintrag
SSLCTX = ssl.create_default_context()

def b64url(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def load_tokens():
    try: return json.load(open(TOKENS_FILE))
    except Exception: return {}

def save_tokens(t): json.dump(t, open(TOKENS_FILE, "w"), indent=2)

def decompress(enc, raw):
    enc = (enc or "").lower().strip()
    try:
        if enc == "gzip": import gzip; return gzip.decompress(raw)
        if enc == "deflate":
            import zlib
            try: return zlib.decompress(raw)
            except Exception: return zlib.decompress(raw, -zlib.MAX_WBITS)
        if enc == "br":
            try: import brotli
            except Exception: import brotlicffi as brotli
            return brotli.decompress(raw)
        if enc == "zstd":
            import zstandard
            return zstandard.ZstdDecompressor().decompress(raw)
    except Exception:
        return raw
    return raw

def http_call(method, url, headers=None, data=None, timeout=40):
    headers = dict(headers or {})
    headers.setdefault("Accept-Encoding", "gzip, deflate, br, zstd")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    def finish(status, h, raw):
        return status, h, decompress(h.get("Content-Encoding"), raw)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSLCTX) as r:
            return finish(r.status, dict(r.headers), r.read())
    except urllib.error.HTTPError as e:
        return finish(e.code, dict(e.headers), e.read())
    except Exception as e:
        return 0, {}, str(e).encode()

def token_request(form):
    body = urllib.parse.urlencode(form).encode()
    basic = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    st, _, raw = http_call("POST", ISSUER + "connect/token", {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": "Basic " + basic,
    }, body)
    try: j = json.loads(raw)
    except Exception: j = {"raw": raw.decode(errors="replace")}
    return st, j

def exchange_code(code, state=None):
    """Tauscht einen Authorization Code gegen Tokens. Gibt (http_status, dict).
    Der passende PKCE Verifier wird ueber state zugeordnet, sonst der neueste."""
    p = PENDING.get(state) if state else None
    if not p:
        # Rueckfall auf den neuesten offenen Login
        p = max(PENDING.values(), key=lambda x: x["at"]) if PENDING else None
    if not p:
        return 400, {"error": "Kein offener Login gefunden, bitte Login neu starten"}
    st, j = token_request({"grant_type": "authorization_code", "client_id": CLIENT_ID,
                           "code": code, "redirect_uri": REDIRECT,
                           "code_verifier": p["verifier"]})
    if st != 200 or "access_token" not in j:
        err = j.get("error") or ("HTTP " + str(st))
        desc = j.get("error_description") or (j.get("raw", "")[:120] if isinstance(j, dict) else "")
        return (st or 400), {"error": "Token Exchange fehlgeschlagen",
                             "oauth_error": err, "oauth_desc": desc, "detail": j}
    if state in PENDING: del PENDING[state]
    j["_expires_at"] = time.time() + j.get("expires_in", 3600)
    j["_country"] = p.get("country", "DE"); j["_lang"] = p.get("lang", "de")
    save_tokens(j)
    return 200, {"ok": True, "expires_in": j.get("expires_in"), "scope": j.get("scope")}

def ensure_fresh():
    """Erneuert das Access Token bei Bedarf. Gibt das Token oder None."""
    t = load_tokens()
    if not t.get("access_token"): return None
    if t.get("_expires_at", 0) - 30 > time.time(): return t
    if not t.get("refresh_token"): return t
    st, j = token_request({"grant_type": "refresh_token", "client_id": CLIENT_ID,
                           "refresh_token": t["refresh_token"]})
    if st == 200 and "access_token" in j:
        t.update(j); t["_expires_at"] = time.time() + j.get("expires_in", 3600)
        save_tokens(t)
    return t

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)): body = json.dumps(body, ensure_ascii=False).encode()
        elif isinstance(body, str): body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        n = int(self.headers.get("Content-Length", "0") or "0")
        if not n: return {}
        try: return json.loads(self.rfile.read(n))
        except Exception: return {}

    # ---- static
    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/api/auth/status":
            t = load_tokens()
            return self._send(200, {
                "authenticated": bool(t.get("access_token")),
                "expires_at": t.get("_expires_at"),
                "scope": t.get("scope"),
                "country": t.get("_country"), "lang": t.get("_lang"),
                "last_catch": STATE.get("last_catch"),
            })
        if p == "/api/auth/catch":
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            return self.auth_catch(q.get("url", [""])[0])
        if p == "/" or p == "": p = "/index.html"
        fp = os.path.normpath(os.path.join(HERE, p.lstrip("/")))
        if not fp.startswith(HERE) or not os.path.isfile(fp):
            return self._send(404, {"error": "not found"})
        ctype = {".html": "text/html; charset=utf-8", ".json": "application/json",
                 ".js": "text/javascript", ".css": "text/css"}.get(os.path.splitext(fp)[1], "text/plain")
        self._send(200, open(fp, "rb").read(), ctype)

    # ---- api
    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/api/auth/catch":
            n = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(n).decode(errors="replace") if n else ""
            form = urllib.parse.parse_qs(raw)
            return self.auth_catch(form.get("url", [raw])[0])
        body = self._read_json()
        if p == "/api/auth/start":    return self.auth_start(body)
        if p == "/api/auth/exchange": return self.auth_exchange(body)
        if p == "/api/auth/refresh":  return self.auth_refresh()
        if p == "/api/auth/logout":
            try: os.remove(TOKENS_FILE)
            except Exception: pass
            return self._send(200, {"ok": True})
        if p == "/api/proxy":         return self.proxy(body)
        self._send(404, {"error": "not found"})

    def auth_start(self, b):
        verifier = b64url(secrets.token_bytes(64))
        challenge = b64url(hashlib.sha256(verifier.encode()).digest())
        state = b64url(secrets.token_bytes(16))
        country = (b.get("country") or "DE").upper()
        lang = (b.get("lang") or "de").lower()
        PENDING[state] = {"verifier": verifier, "country": country, "lang": lang, "at": time.time()}
        # alte offene Logins aufraeumen, die letzten paar reichen
        for k in sorted(PENDING, key=lambda x: PENDING[x]["at"])[:-5]:
            del PENDING[k]
        q = {"client_id": CLIENT_ID, "response_type": "code", "scope": SCOPE,
             "redirect_uri": REDIRECT, "code_challenge": challenge,
             "code_challenge_method": "S256", "state": state,
             "nonce": b64url(secrets.token_bytes(16)),
             "Country": country, "language": f"{lang}-{country}",
             "track": "false", "force": "false"}
        self._send(200, {"authorize_url": ISSUER + "connect/authorize?" + urllib.parse.urlencode(q)})

    def auth_exchange(self, b):
        raw = (b.get("callback_url") or "").strip()
        # Akzeptiert die volle com.lidlplus.app Adresse, eine beliebige URL mit
        # code Parameter, oder den nackten Code allein.
        q = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
        if "error" in q:
            return self._send(400, {"error": q["error"][0],
                                    "detail": q.get("error_description", [""])[0]})
        code = q.get("code", [None])[0]
        state = q.get("state", [None])[0]
        if not code:
            if raw and "://" not in raw and "=" not in raw and " " not in raw:
                code = raw                      # nackter Code eingefügt
        if not code:
            return self._send(400, {"error": "Kein code gefunden, ganze URL oder nur den code einfügen"})
        st, j = exchange_code(code, state)
        self._send(st, j)

    def auth_catch(self, raw):
        """Nimmt die abgefangene com.lidlplus.app Adresse vom URL Handler entgegen."""
        q = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
        code = q.get("code", [None])[0]
        state = q.get("state", [None])[0]
        if not code:
            STATE["last_catch"] = {"at": time.time(), "ok": False, "msg": "ohne code"}
            return self._send(400, "Kein code in der Adresse", "text/plain; charset=utf-8")
        st, j = exchange_code(code, state)
        msg = "angemeldet" if j.get("ok") else \
              (str(j.get("error", "")) + (": " + j.get("oauth_error", "") if j.get("oauth_error") else ""))
        STATE["last_catch"] = {"at": time.time(), "ok": bool(j.get("ok")), "msg": msg}
        msg = "Angemeldet. Du kannst zur Lidl Plus API zurueck." if j.get("ok") \
              else ("Fehler: " + str(j.get("error", "")))
        self._send(200 if j.get("ok") else 400, msg, "text/plain; charset=utf-8")

    def auth_refresh(self):
        t = load_tokens()
        if not t.get("refresh_token"):
            return self._send(400, {"error": "Kein refresh_token"})
        st, j = token_request({"grant_type": "refresh_token", "client_id": CLIENT_ID,
                               "refresh_token": t["refresh_token"]})
        if st != 200 or "access_token" not in j:
            return self._send(st or 400, {"error": "Refresh fehlgeschlagen", "detail": j})
        t.update(j); t["_expires_at"] = time.time() + j.get("expires_in", 3600)
        save_tokens(t)
        self._send(200, {"ok": True, "expires_in": j.get("expires_in")})

    def proxy(self, b):
        url = b.get("url", "")
        method = (b.get("method") or "GET").upper()
        if not url.startswith("https://"):
            return self._send(400, {"error": "Nur https Ziele erlaubt"})
        t = ensure_fresh() or {}
        headers = {
            "App": "com.lidl.eci.lidlplus", "App-Version": APP_VERSION,
            "Operating-System": "Android",
            "Accept-Language": f"{t.get('_lang','de')}-{t.get('_country','DE')}",
            "Accept": "application/json",
        }
        if t.get("access_token") and b.get("auth", True):
            headers["Authorization"] = "Bearer " + t["access_token"]
        for k, v in (b.get("headers") or {}).items():
            if v is not None and str(v) != "": headers[k] = str(v)
        data = None
        raw_body = b.get("body")
        if raw_body not in (None, ""):
            if isinstance(raw_body, (dict, list)):
                data = json.dumps(raw_body).encode(); headers.setdefault("Content-Type", "application/json")
            else:
                data = str(raw_body).encode()
        t0 = time.time()
        st, rh, rb = http_call(method, url, headers, data)
        retried = False
        # Manche Endpunkte verlangen Accept-Language mit genau 2 Zeichen.
        # Bei 400 mit Sprach-Laengenfehler einmal mit Kurzform nachfassen.
        al = headers.get("Accept-Language", "")
        if st == 400 and "-" in al and re.search(rb"(?i)language", rb or b"") and (b"2" in (rb or b"")):
            short_al = al.split("-")[0]
            if short_al and short_al != al:
                h2 = dict(headers); h2["Accept-Language"] = short_al
                st2, rh2, rb2 = http_call(method, url, h2, data)
                if st2 != 400:
                    st, rh, rb, headers, retried = st2, rh2, rb2, h2, True
        dt = int((time.time() - t0) * 1000)
        ct = rh.get("Content-Type", "")
        try: parsed = json.loads(rb); text = None
        except Exception: parsed = None; text = rb.decode(errors="replace")
        allow = rh.get("Allow") or rh.get("allow")
        self._send(200, {"status": st, "ms": dt, "content_type": ct,
                         "json": parsed, "text": text, "retried_short_lang": retried,
                         "allow": allow,
                         "sent_headers": {k: ("Bearer ..." if k == "Authorization" else v)
                                          for k, v in headers.items()},
                         "final_url": url})

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    print(f"Lidl Plus API auf http://127.0.0.1:{PORT}")
    print("Beenden mit Strg C")
    Server(("127.0.0.1", PORT), H).serve_forever()
