import re, joblib
from checks import check_url

model = joblib.load("text_model.pkl")
URL_RE = re.compile(r"(https?://\S+|\b(?:[\w-]+\.)+(?:com|in|xyz|top|click|co|link|icu|buzz)\b\S*|\b(?:bit\.ly|tinyurl\.com|cutt\.ly)/\S+)")

def label_for(score):
    return "Dangerous" if score >= 70 else "Suspicious" if score >= 40 else "Likely safe"

def analyze(text, expecting_to_receive=False):
    reasons = []
    text_score = int(model.predict_proba([text])[0][1] * 100)
    if text_score > 60:
        reasons.append("Message wording matches known scam patterns (urgency, threats, rewards)")
    url_scores = []
    for url in URL_RE.findall(text):
        s, r = check_url(url.rstrip(".,)"))
        url_scores.append(s); reasons += r
    if re.search(r"\bpin\b", text, re.I) and re.search(r"receive|refund|reward|cashback|accept|claim", text, re.I) \
       and not re.search(r"never|do not|don't", text, re.I):
        reasons.append("Asks for your PIN to give you money. This is always a scam.")
        text_score = max(text_score, 90)
    final = max([text_score] + url_scores)
    if url_scores and text_score > 60:
        final = min(100, final + 10)
    return {"score": final, "label": label_for(final), "reasons": reasons or ["No warning signs found"]}
