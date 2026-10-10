# Scam Shield - UPI and SMS Scam Detector

Checks an SMS, link or UPI QR code and returns a risk score with plain-language reasons.

## Run it
    python -m venv venv
    venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
    pip install -r requirements.txt
    python make_data.py            (creates data/indian.csv)
    python train.py                (creates text_model.pkl)
    python test_cases.py           (10 fresh test messages)
    uvicorn app:app --reload       (open http://localhost:8000)

Demo QR images: demo_fake_qr.png (tick "I am expecting to receive money" -> red) and demo_genuine_qr.png (green).

## How it works
1. Text model (TF-IDF + logistic regression) scores scam wording.
2. URL rules: shorteners, bad domain endings, fake bank lookalikes, raw IPs, no HTTPS.
3. UPI rules: pay-vs-receive mismatch, large amounts, missing payee, "PIN to receive money".
4. The worst signal wins, with a small bonus when text and link both look bad.

## Improve it
- Add your own messages to data/indian.csv (or put Kaggle spam.csv in data/) and retrain.
- Add Hindi/Odia examples, a Telegram bot, a domain-age check.
- Training data is template-generated, so the 100% training score is optimistic. Report the fresh-test number honestly.
