import os, pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("data/indian.csv")
if os.path.exists("data/spam.csv"):   # optional: Kaggle SMS Spam Collection
    a = pd.read_csv("data/spam.csv", encoding="latin-1")[["v1", "v2"]]
    a.columns = ["label", "text"]
    df = pd.concat([a, df], ignore_index=True)
    print("Using spam.csv too")
y = (df.label == "spam").astype(int)
Xtr, Xte, ytr, yte = train_test_split(df.text, y, test_size=0.2, stratify=y, random_state=1)
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), lowercase=True),
                      LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(Xtr, ytr)
print(classification_report(yte, model.predict(Xte)))
print("NOTE: data is template-generated, so this score is optimistic. Run test_cases.py for fresh messages.")
joblib.dump(model, "text_model.pkl")
