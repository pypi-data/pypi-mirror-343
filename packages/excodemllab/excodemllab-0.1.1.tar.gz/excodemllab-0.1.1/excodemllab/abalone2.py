import pandas as pd

data_path = r'abalone/abalone.data'

columns = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight',
           'Shucked weight', 'Viscera weight', 'Shell weight', 'Rings']

df = pd.read_csv(data_path, header=None, names=columns)

df.to_csv("abalone2.csv", index=False)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


df = pd.read_csv("abalone2.csv")

df['Age_Class'] = (df['Rings'] > 10).astype(int)


X = df[['Length', 'Diameter', 'Height', 'Whole weight', 
        'Shucked weight', 'Viscera weight', 'Shell weight']]
y = df['Age_Class']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1] 


mse_class = mean_squared_error(y_test, y_pred)
r2_class = r2_score(y_test, y_pred)

mse_prob = mean_squared_error(y_test, y_pred_prob)
r2_prob = r2_score(y_test, y_pred_prob)

print(f"\nForced Metrics (using class labels):")
print(f"MSE (labels): {mse_class:.4f}")
print(f"R² Score (labels): {r2_class:.4f}")

print(f"\nOptional Metrics (using probabilities):")
print(f"MSE (probabilities): {mse_prob:.4f}")
print(f"R² Score (probabilities): {r2_prob:.4f}")


accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(class_report)
   
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Young (0)', 'Old (1)'],
            yticklabels=['Young (0)', 'Old (1)'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
# plt.tight_layout()
plt.show()

sns.countplot(x='Age_Class', data=df)
plt.title("Distribution of Age Classes (Young=0, Old=1)")
plt.xlabel("Age Class")
plt.ylabel("Count")
# plt.tight_layout()
plt.show()



