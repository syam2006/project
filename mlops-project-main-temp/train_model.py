import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Generate a reproducible student dataset (500 students)
rng = np.random.default_rng(42)
n = 500
hours = rng.uniform(0, 12, n)
attendance = rng.uniform(40, 100, n)
previous = rng.uniform(30, 100, n)
marks = 5 + 4.0 * hours + 0.20 * attendance + 0.35 * previous + rng.normal(0, 4, n)
marks = np.clip(marks, 0, 100)

df = pd.DataFrame({
    "hours_studied": hours.round(1),
    "attendance": attendance.round(1),
    "previous_marks": previous.round(1),
    "marks": marks.round(1)
})
df.to_csv("students.csv", index=False)
print("Dataset shape:", df.shape)
print(df.head())

X = df[["hours_studied", "attendance", "previous_marks"]]
y = df["marks"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("reg", LinearRegression())
])
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("\nMAE  : {:.3f}".format(mean_absolute_error(y_test, pred)))
print("RMSE : {:.3f}".format(np.sqrt(mean_squared_error(y_test, pred))))
print("R2   : {:.3f}".format(r2_score(y_test, pred)))

joblib.dump(model, "model.pkl")
print("model.pkl created successfully")
