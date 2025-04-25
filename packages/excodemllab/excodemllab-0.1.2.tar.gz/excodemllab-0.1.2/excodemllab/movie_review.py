import os
import pandas

l = r'Movie review\aclImdb\train'
data = []

for label in ["pos", "neg"]:
    folder_path = os.path.join(l,label)
    for filename in os.listdir(folder_path):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                data.append((content, label))
                
df = pandas.DataFrame(data, columns=["text", "label"])
df.to_csv("movie_review.csv", index=False)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import nltk
from nltk.corpus import stopwords

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

nltk.download("stopwords")

df = pd.read_csv("movie_review.csv")
df["label"] = df["label"].map({ "pos":1, "neg":0 })

print(df.head(5))
print(df["label"].isnull().sum())

stop_words = set(stopwords.words("english"))

def preprocess_text(text):
  text = text.lower()
  text = re.sub(r"\<.*?\>", "", text)
  text = re.sub(r"https?://\S+|www\.\S+", "", text)
  text = re.sub(r"[^a-zA-Z]", " ", text)
  words = text.split()
  words = [word for word in words if word not in stop_words]
  return " ".join(words)

df["text"] = df["text"].apply(preprocess_text)

x_train, x_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size = 0.2, random_state=42)

t = TfidfVectorizer()
x_train = t.fit_transform(x_train)
x_test = t.transform(x_test)

d = DecisionTreeClassifier(max_depth=10, random_state=42)
d.fit(x_train, y_train)
d_pred = d.predict(x_test)

print("Accuracy : ", accuracy_score(y_test, d_pred))
print("Report : ", classification_report(y_test, d_pred))
print("matrix : ", confusion_matrix(y_test, d_pred))

r = RandomForestClassifier(max_depth=10, random_state=42)
r.fit(x_train, y_train)
r_pred = r.predict(x_test)

print("Accuracy : ", accuracy_score(y_test, r_pred))
print("Report : ", classification_report(y_test, r_pred))
print("matrix : ", confusion_matrix(y_test, r_pred))