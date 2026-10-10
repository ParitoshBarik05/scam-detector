import re
from urllib.parse import urlparse, parse_qs
import tldextract, cv2, numpy as np

extract = tldextract.TLDExtract(suffix_list_urls=())  # offline-safe
SHORTENERS = {"bit.ly", "tinyurl.com", "cutt.ly", "rb.gy", "t.co"}
BAD_TLDS = {"xyz", "top", "click", "icu", "buzz", "tk", "site", "link"}
BRANDS = ["sbi", "hdfc", "icici", "paytm", "phonepe", "gpay", "npci", "axis", "pnb"]
OFFICIAL = {"sbi.co.in", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com", "paytm.com",
            "phonepe.com", "npci.org.in", "axisbank.com", "pnbindia.in"}

def check_url(url):
    score, reasons = 0, []
    host = urlparse(url if "//" in url else "http://" + url).hostname or ""
    ext = extract(host)
    domain = f"{ext.domain}.{ext.suffix}"
    if domain in SHORTENERS:
        score += 35; reasons.append("Shortened link hides the real destination")
    if ext.suffix in BAD_TLDS:
        score += 30; reasons.append(f"Uses a suspicious domain ending (.{ext.suffix})")
    if re.fullmatch(r"[\d.]+", host):
        score += 40; reasons.append("Link uses a raw IP address")
    if any(b in host for b in BRANDS) and domain not in OFFICIAL:
        score += 45; reasons.append("Pretends to be a bank/payment brand but is not the official site")
    if host.count("-") >= 2:
        score += 10; reasons.append("Many hyphens in the domain, common in fake sites")
    if url.startswith("http://"):
        score += 10; reasons.append("Not using HTTPS")
    return min(score, 100), reasons

def decode_qr(image_bytes):
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return ""
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return data

def check_upi(link, expecting_to_receive=False):
    score, reasons = 0, []
    if not link.lower().startswith("upi://"):
        s, r = check_url(link)
        return s, r or ["QR contains a normal link, not a UPI payment"]
    q = {k: v[0] for k, v in parse_qs(urlparse(link).query).items()}
    try:
        amount = float(q.get("am", 0) or 0)
    except ValueError:
        amount = 0
    if expecting_to_receive and amount > 0:
        score += 80; reasons.append("You expect to RECEIVE money, but this code makes you PAY. Receiving never needs a PIN or a payment.")
    if amount >= 10000:
        score += 20; reasons.append(f"Large amount requested (Rs {amount:,.0f})")
    if "pn" not in q:
        score += 15; reasons.append("No payee name attached")
    return min(score, 100), reasons
