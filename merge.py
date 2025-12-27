import base64, re
from urllib.request import Request, urlopen

URLS_FILE = "urls.txt"
OUT = "merged.txt"

def looks_b64(s: str) -> bool:
    s = s.strip()
    if len(s) < 20:
        return False
    return re.fullmatch(r"[A-Za-z0-9+/=\s_-]+", s) is not None

def b64_decode_flexible(s: str) -> str:
    s = s.strip().replace("-", "+").replace("_", "/")
    s += "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s).decode("utf-8", errors="ignore")

def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore").strip()

urls = [u.strip() for u in open(URLS_FILE, encoding="utf-8") if u.strip()]
all_lines = []

for url in urls:
    raw = fetch(url)
    decoded = b64_decode_flexible(raw) if looks_b64(raw) else raw
    for line in decoded.splitlines():
        line = line.strip()
        if line.startswith(("vmess://","vless://","trojan://","ss://","ssr://","hy2://","hysteria://","tuic://")):
            all_lines.append(line)

# remove duplicates, keep order
seen = set()
uniq = []
for x in all_lines:
    if x not in seen:
        seen.add(x)
        uniq.append(x)

plain = "\n".join(uniq) + "\n"
out_b64 = base64.b64encode(plain.encode()).decode()

open(OUT, "w", encoding="utf-8").write(out_b64)
print("Merged lines:", len(uniq))
