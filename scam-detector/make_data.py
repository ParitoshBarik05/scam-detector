"""Generates an Indian-style scam/genuine SMS dataset -> data/indian.csv"""
import random, csv
random.seed(7)
banks = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "Paytm", "PhonePe", "Bank of Baroda"]
bad = ["{b}-kyc-update.xyz", "{b}-secure.top", "bit.ly/{r}", "tinyurl.com/{r}", "{b}-verify-login.click", "cutt.ly/{r}", "upi-reward.icu"]
SCAM = [
 "Dear customer your {B} account will be blocked today. Update KYC now: http://{u}",
 "{B} ALERT: Your KYC has expired. Account suspended in 24 hours. Click http://{u} to verify",
 "Your electricity will be disconnected tonight 9:30pm due to unpaid bill. Call {p} immediately",
 "Congratulations! You won Rs {a} cashback. Enter your UPI PIN to receive the money",
 "Your parcel is held at the warehouse. Pay Rs {s} delivery fee at http://{u} to release it",
 "Dear user, your {B} credit card reward points worth Rs {a} expire today. Redeem: http://{u}",
 "You have received a refund of Rs {a}. Enter your PIN to accept the refund",
 "URGENT: Your PAN is not linked. {B} account will be frozen. Update at http://{u}",
 "Part time job offer! Earn Rs {a} daily from home. Message on WhatsApp {p} now",
 "Your SIM will be deactivated in 2 hours. Complete re-verification: http://{u}",
 "{B}: Unusual login detected. Verify your identity immediately http://{u} or account will be locked",
 "Claim your free gift and lottery prize of Rs {a}. Share your card number and OTP to claim",
 "Income tax refund of Rs {a} approved. Submit bank details at http://{u}",
 "Send Rs {s} to unlock your prize of Rs {a}. Limited time offer, act now",
]
HAM = [
 "Your OTP for login is {o}. Do not share it with anyone. -{B}",
 "Rs {a} debited from A/c XX{n} on 10-Oct. Avl bal Rs {a2}. -{B}",
 "Rs {a} credited to your A/c XX{n} on 09-Oct via UPI. Ref {o}. -{B}",
 "Your order has been shipped and will arrive on Monday. -Amazon",
 "{o} is your verification code for {B}. Valid for 10 minutes.",
 "Your electricity bill of Rs {a} is generated. Due date 25-Oct. Pay via the official app. -Odisha Discom",
 "Hi, are we still meeting for lunch tomorrow at 1?",
 "Your Swiggy order is out for delivery. Arriving in 15 minutes.",
 "Thanks for paying Rs {a} to Ramesh Kumar using UPI. Txn ID {o}.",
 "Reminder: your EMI of Rs {a} is due on 5th. Ensure sufficient balance in A/c XX{n}. -{B}",
 "Mom, I reached home safely. Will call you after dinner.",
 "Your appointment with Dr. Sharma is confirmed for Saturday 11:00 AM.",
 "Dear customer, never share your PIN or OTP with anyone. {B} will never ask for it.",
 "Your cylinder booking is confirmed. Delivery within 3 days. Ref {o}.",
 "Can you send me the notes from class? I missed it.",
 "Happy birthday! Have a great day, let's catch up this weekend.",
 "Did you reach the station? Call me when you get there.",
 "Please bring milk and bread on your way back home.",
 "The movie starts at 7. I will book the tickets, you come directly.",
 "Hey, are you free tomorrow? Let's discuss the project.",
 "Thanks a lot for your help today, really appreciate it!",
 "Dinner is ready, come down soon.",
 "Meeting moved to 4pm. Agenda attached in the mail. Please check https://www.google.com/",
]
def fill(t, scam):
    b = random.choice(banks); r = "".join(random.choices("abcdefgh12345", k=6))
    u = random.choice(bad).format(b=b.split()[0].lower(), r=r)
    return t.format(B=b, u=u, p="9"+"".join(random.choices("0123456789", k=9)),
        a=random.choice([499, 1200, 2500, 5000, 10000, 25000, 50000]), s=random.choice([9, 29, 49, 99]),
        a2=random.randint(1000, 90000), n=random.randint(1000, 9999), o=random.randint(100000, 999999))
rows = [("spam", fill(random.choice(SCAM), 1)) for _ in range(400)] + [("ham", fill(random.choice(HAM), 0)) for _ in range(400)]
random.shuffle(rows)
with open("data/indian.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["label", "text"]); w.writerows(rows)
print(len(rows), "rows written")
