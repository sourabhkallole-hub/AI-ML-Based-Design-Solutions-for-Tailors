import pandas as pd
import joblib

# ===== Load Saved Artifacts =====
model = joblib.load("fashion_rf_model.pkl")
kmeans = joblib.load("body_type_kmeans.pkl")
le_gender = joblib.load("gender_encoder.pkl")
le_occasion = joblib.load("occasion_encoder.pkl")
le_outfit = joblib.load("recommended_outfit_encoder.pkl")
le_age_group = joblib.load("age_group_encoder.pkl")

# ===== Input Sample =====
input_data = {
    "gender": "Female",
    "age": 28,
    "height_cm": 160,
    "chest_cm": 85,
    "waist_cm": 70,
    "hips_cm": 92,
    "shoulder_cm": 40,
    "occasion": "Wedding"
}

# ===== Preprocessing =====
input_data["chest_waist_ratio"] = input_data["chest_cm"] / input_data["waist_cm"]
input_data["age_group"] = pd.cut([input_data["age"]], bins=[0, 12, 18, 35, 50, 100],
                                 labels=["Kid", "Teen", "Young", "Adult", "Senior"])[0]
input_data["gender_encoded"] = le_gender.transform([input_data["gender"]])[0]
input_data["occasion_encoded"] = le_occasion.transform([input_data["occasion"]])[0]
input_data["age_group_encoded"] = le_age_group.transform([input_data["age_group"]])[0]

cluster_df = pd.DataFrame([input_data])[["height_cm", "chest_cm", "waist_cm"]]
input_data["body_type_cluster"] = kmeans.predict(cluster_df)[0]

# ===== Final Feature Vector =====
X_test = pd.DataFrame([{
    "gender_encoded": input_data["gender_encoded"],
    "age": input_data["age"],
    "height_cm": input_data["height_cm"],
    "chest_cm": input_data["chest_cm"],
    "waist_cm": input_data["waist_cm"],
    "hips_cm": input_data["hips_cm"],
    "shoulder_cm": input_data["shoulder_cm"],
    "occasion_encoded": input_data["occasion_encoded"],
    "chest_waist_ratio": input_data["chest_waist_ratio"],
    "age_group_encoded": input_data["age_group_encoded"],
    "body_type_cluster": input_data["body_type_cluster"]
}])

# ===== Predict =====
predicted_label = model.predict(X_test)[0]
predicted_outfit = le_outfit.inverse_transform([predicted_label])[0]

print("🎯 Recommended Outfit:", predicted_outfit)
