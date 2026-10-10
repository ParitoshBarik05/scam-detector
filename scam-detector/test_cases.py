"""Fresh hand-written messages NOT in the training generator."""
from analyzer import analyze
CASES = [
 ("Sir your Jio SIM KYC pending, will be blocked tonight. Call 9876501234 now", "bad"),
 ("Dear SBI user, update PAN immediately at http://sbi-pan-verify.top or account freezes", "bad"),
 ("You are selected for a Rs 50000 reward! Enter UPI PIN to receive your prize", "bad"),
 ("Your courier is stuck. Pay Rs 25 at bit.ly/3xYz12 to reschedule delivery", "bad"),
 ("Electricity connection will be cut at 10pm today, contact officer 9812345678", "bad"),
 ("123456 is your OTP for HDFC Bank NetBanking. Never share it with anyone.", "ok"),
 ("Rs 340 debited from A/c XX1122 at Big Bazaar. Avl bal Rs 12,300. -ICICI Bank", "ok"),
 ("Hey, can you send me the notes from yesterday's class?", "ok"),
 ("Your Zomato order #8841 has been delivered. Enjoy your meal!", "ok"),
 ("Your train PNR 4521897650 is confirmed. Coach S3, berth 24. Happy journey.", "ok"),
]
good = 0
for text, truth in CASES:
    r = analyze(text); flagged = r["score"] >= 40
    hit = flagged == (truth == "bad"); good += hit
    print(("PASS" if hit else "FAIL"), r["label"].ljust(11), r["score"], "|", text[:60])
print(f"\n{good}/{len(CASES)} correct on fresh messages")
