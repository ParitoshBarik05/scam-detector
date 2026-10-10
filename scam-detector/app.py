from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from analyzer import analyze, label_for
from checks import decode_qr, check_upi

app = FastAPI(title="Scam Shield")

class Msg(BaseModel):
    text: str
    expecting_to_receive: bool = False

@app.post("/scan")
def scan(m: Msg):
    return analyze(m.text, m.expecting_to_receive)

@app.post("/scan-qr")
async def scan_qr(file: UploadFile, expecting_to_receive: bool = False):
    link = decode_qr(await file.read())
    if not link:
        return {"score": 0, "label": "Unreadable", "reasons": ["Could not read a QR code. Try a clearer image."]}
    score, reasons = check_upi(link, expecting_to_receive)
    return {"score": score, "label": label_for(score), "reasons": reasons or ["No warning signs found"], "decoded": link}

app.mount("/", StaticFiles(directory="static", html=True))
