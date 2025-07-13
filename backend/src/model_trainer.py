import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from feature_engineering import InvoiceFeatureExtractor

# Load data
invoice_data = pd.read_csv('data/invoice_data.csv')

# Feature extraction
extractor = InvoiceFeatureExtractor()
features = extractor.extract_features(invoice_data)
feature_names = extractor.get_feature_names()

# Labels
labels = invoice_data['is_fake']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

# Train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate Random Forest model
rf_predictions = rf_model.predict(X_test)
print("Random Forest Classifier Report:")
print(classification_report(y_test, rf_predictions))
print("Accuracy:", accuracy_score(y_test, rf_predictions))

# Train XGBoost model
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train, y_train)

# Evaluate XGBoost model
xgb_predictions = xgb_model.predict(X_test)
print("XGBoost Classifier Report:")
print(classification_report(y_test, xgb_predictions))
print("Accuracy:", accuracy_score(y_test, xgb_predictions))

# Save models
joblib.dump(rf_model, 'models/random_forest_model.pkl')
joblib.dump(xgb_model, 'models/xgb_model.pkl')
print("Models saved to 'models/' directory.")
