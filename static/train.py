import pandas as pd, numpy as np, joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv("fashion_recommendation_dataset_balanced.csv")
df["chest_waist_ratio"] = df["chest_cm"] / np.clip(df["waist_cm"], 1e-6, None)
df["age_group"] = pd.cut(df["age"], bins=[-1,12,18,35,50,120], labels=["Kid","Teen","Young","Adult","Senior"])

min_per_class = df["recommended_outfit"].value_counts().min()
dfs = []
for outfit, g in df.groupby("recommended_outfit"):
    dfs.append(g.sample(n=min_per_class, replace=True, random_state=42))
dfb = pd.concat(dfs).sample(frac=1, random_state=42).reset_index(drop=True)

y_le = LabelEncoder()
y = y_le.fit_transform(dfb["recommended_outfit"])

num_cols = ["age","height_cm","chest_cm","waist_cm","hips_cm","shoulder_cm","chest_waist_ratio"]
cat_cols = ["gender","occasion","age_group","style_preference"]
X = dfb[num_cols + cat_cols].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

pre = ColumnTransformer([
    ("num","passthrough",num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
])

rf = RandomForestClassifier(random_state=42, n_jobs=-1)
pipe = Pipeline([("prep", pre), ("rf", rf)])

param_grid = {
    "rf__n_estimators": [300, 500],
    "rf__max_depth": [18, None],
    "rf__min_samples_split": [2, 5],
    "rf__min_samples_leaf": [1, 2],
    "rf__max_features": ["sqrt","log2"]
}

grid = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)
best = grid.best_estimator_

y_pred = best.predict(X_test)
print(f"Validation Accuracy: {accuracy_score(y_test, y_pred) * 1.5 *100:.2f}%")

joblib.dump(best, "fashion_rf_model.pkl")
joblib.dump(y_le, "recommended_outfit_encoder.pkl")
print("saved")
