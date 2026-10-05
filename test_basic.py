#!/usr/bin/env python3
"""Kleiner Selbsttest ohne Netzwerk. Aufruf: python3 test_basic.py"""
import base64, gzip, hashlib, importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    spec = importlib.util.spec_from_file_location("srv", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_pkce(srv):
    v = srv.b64url(os.urandom(64))
    c = srv.b64url(hashlib.sha256(v.encode()).digest())
    assert c == base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()
    assert "=" not in v and "+" not in v and "/" not in v
    print("ok pkce")

def test_decompress(srv):
    raw = b'{"hallo":"welt"}'
    assert srv.decompress("gzip", gzip.compress(raw)) == raw
    assert srv.decompress("identity", raw) == raw
    assert srv.decompress(None, raw) == raw
    print("ok decompress")

def test_endpoints():
    d = json.load(open(os.path.join(HERE, "webapp", "endpoints.json")))
    assert len(d["endpoints"]) > 100
    assert d["models"] and isinstance(d["models"], dict)
    assert d["rn"] and isinstance(d["rn"], list)
    for e in d["endpoints"]:
        assert e["verb"] in ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
    print(f"ok endpoints ({len(d['endpoints'])}, models {len(d['models'])})")

def test_postman():
    p = json.load(open(os.path.join(HERE, "webapp", "postman_collection.json")))
    assert p["info"]["name"] and p["item"]
    print(f"ok postman ({sum(len(f['item']) for f in p['item'])} requests)")

if __name__ == "__main__":
    srv = load(os.path.join(HERE, "webapp", "server.py"))
    test_pkce(srv); test_decompress(srv); test_endpoints(); test_postman()
    print("alle Tests bestanden")
