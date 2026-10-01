import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import joblib
import os
import warnings

warnings.filterwarnings('ignore')

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

print("=" * 80)
print("CHURNWISE - ML MODEL TRAINING PIPELINE")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ============================================================================
print("\n[1/5] Loading and preparing dataset...")

# Check if dataset exists
if not os.path.exists('../dataset/customer_churn.csv'):
    print("Creating synthetic customer churn dataset...")
    # Create synthetic dataset for demonstration
    np.random.seed(42)
    
    n_samples = 7043
    
    data = {
        'customerID': [f'CUST_{i:05d}' for i in range(n_samples)],
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples, p=[0.84, 0.16]),
        'Partner': np.random.choice(['Yes', 'No'], n_samples, p=[0.48, 0.52]),
        'Dependents': np.random.choice(['Yes', 'No'], n_samples, p=[0.30, 0.70]),
        'tenure': np.random.randint(1, 72, n_samples),
        'PhoneService': np.random.choice(['Yes', 'No'], n_samples, p=[0.90, 0.10]),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples, p=[0.44, 0.42, 0.14]),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.28, 0.50, 0.22]),
        'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.25, 0.53, 0.22]),
        'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.22, 0.56, 0.22]),
        'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.27, 0.51, 0.22]),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.35, 0.43, 0.22]),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples, p=[0.34, 0.44, 0.22]),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.55, 0.20, 0.25]),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples, p=[0.59, 0.41]),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples),
        'MonthlyCharges': np.random.uniform(18, 118, n_samples),
        'TotalCharges': np.random.uniform(18, 8500, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create churn column based on realistic patterns
    churn_prob = []
    for i in range(n_samples):
        prob = 0.26  # baseline churn rate
        
        # Increase churn for month-to-month contracts
        if df.loc[i, 'Contract'] == 'Month-to-month':
            prob += 0.25
        elif df.loc[i, 'Contract'] == 'One year':
            prob -= 0.10
        elif df.loc[i, 'Contract'] == 'Two year':
            prob -= 0.15
        
        # Short tenure increases churn
        if df.loc[i, 'tenure'] < 12:
            prob += 0.20
        elif df.loc[i, 'tenure'] > 48:
            prob -= 0.15
        
        # No online security/backup increases churn
        if df.loc[i, 'OnlineSecurity'] == 'No':
            prob += 0.10
        if df.loc[i, 'OnlineBackup'] == 'No':
            prob += 0.08
        
        # Tech support reduces churn
        if df.loc[i, 'TechSupport'] == 'Yes':
            prob -= 0.15
        
        # Fiber optic increases churn (quality issues)
        if df.loc[i, 'InternetService'] == 'Fiber optic':
            prob += 0.10
        
        # High monthly charges increase churn
        if df.loc[i, 'MonthlyCharges'] > 80:
            prob += 0.15
        
        # Senior citizens have higher churn
        if df.loc[i, 'SeniorCitizen'] == 1:
            prob += 0.10
        
        # Clip probability to [0, 1]
        prob = max(0, min(1, prob))
        churn_prob.append(prob)
    
    df['Churn'] = [np.random.rand() < p for p in churn_prob]
    df['Churn'] = df['Churn'].astype(int)
    
    # Save dataset
    os.makedirs('../dataset', exist_ok=True)
    df.to_csv('../dataset/customer_churn.csv', index=False)
    print(f"✓ Created synthetic dataset with {n_samples} samples")
else:
    df = pd.read_csv('../dataset/customer_churn.csv')
    print(f"✓ Loaded dataset with {len(df)} samples")

print(f"Dataset shape: {df.shape}")
print(f"\nTarget variable distribution:")
print(df['Churn'].value_counts())
print(f"Churn rate: {df['Churn'].mean():.2%}")

# ============================================================================
# STEP 2: DATA PREPROCESSING
# ============================================================================
print("\n[2/5] Preprocessing data...")

# Make a copy for processing
df_processed = df.copy()

# Drop customerID and other non-predictive columns
df_processed = df_processed.drop(['customerID'], axis=1)

# Handle missing values in TotalCharges
df_processed['TotalCharges'] = pd.to_numeric(df_processed['TotalCharges'], errors='coerce')
df_processed['TotalCharges'].fillna(df_processed['TotalCharges'].mean(), inplace=True)

# Identify categorical and numerical columns
categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df_processed.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical_cols.remove('Churn')  # Separate target variable

print(f"Categorical features: {len(categorical_cols)}")
print(f"Numerical features: {len(numerical_cols)}")

# Encode categorical variables
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col])
    label_encoders[col] = le

# Separate features and target
X = df_processed.drop('Churn', axis=1)
y = df_processed['Churn']

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, 'model/scaler.pkl')
print("✓ Scaler saved to model/scaler.pkl")

# ============================================================================
# STEP 3: TRAIN MODELS
# ============================================================================
print("\n[3/5] Training machine learning models...")

# Train Random Forest
print("\n  Training Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
rf_model.fit(X_train_scaled, y_train)
print("  ✓ Random Forest trained")

# Train Logistic Regression
print("\n  Training Logistic Regression...")
lr_model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)
lr_model.fit(X_train_scaled, y_train)
print("  ✓ Logistic Regression trained")

# ============================================================================
# STEP 4: EVALUATE MODELS
# ============================================================================
print("\n[4/5] Evaluating model performance...")

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """Evaluate and print model metrics"""
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)
    roc_auc = roc_auc_score(y_test, y_test_proba)
    
    print(f"\n  {model_name} Results:")
    print(f"  " + "-" * 50)
    print(f"  Training Accuracy:  {train_acc:.4f}")
    print(f"  Test Accuracy:      {test_acc:.4f}")
    print(f"  Precision:          {precision:.4f}")
    print(f"  Recall:             {recall:.4f}")
    print(f"  F1-Score:           {f1:.4f}")
    print(f"  ROC-AUC:            {roc_auc:.4f}")
    
    # Classification report
    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_test_pred, target_names=['No Churn', 'Churn']))
    
    return {
        'model': model,
        'name': model_name,
        'train_acc': train_acc,
        'test_acc': test_acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc
    }

# Evaluate both models
rf_results = evaluate_model(rf_model, X_train_scaled, X_test_scaled, y_train, y_test, 'Random Forest')
lr_results = evaluate_model(lr_model, X_train_scaled, X_test_scaled, y_train, y_test, 'Logistic Regression')

# ============================================================================
# STEP 5: SELECT AND SAVE BEST MODEL
# ============================================================================
print("\n[5/5] Selecting and saving best model...")

# Compare models using F1 score and ROC-AUC (better for imbalanced data)
print("\n  Model Comparison:")
print(f"  Random Forest - F1: {rf_results['f1']:.4f}, ROC-AUC: {rf_results['roc_auc']:.4f}")
print(f"  Logistic Regression - F1: {lr_results['f1']:.4f}, ROC-AUC: {lr_results['roc_auc']:.4f}")

# Select best model based on F1 score and ROC-AUC
if rf_results['f1'] > lr_results['f1']:
    best_model = rf_results['model']
    best_name = 'Random Forest'
    best_results = rf_results
else:
    best_model = lr_results['model']
    best_name = 'Logistic Regression'
    best_results = lr_results

print(f"\n  ✓ Selected: {best_name}")
print(f"    - F1-Score: {best_results['f1']:.4f}")
print(f"    - ROC-AUC: {best_results['roc_auc']:.4f}")
print(f"    - Precision: {best_results['precision']:.4f}")
print(f"    - Recall: {best_results['recall']:.4f}")

# Save the best model
joblib.dump(best_model, 'model/churn_model.pkl')
print(f"\n  ✓ Model saved to model/churn_model.pkl")

# Save feature names for prediction
feature_names = list(X.columns)
joblib.dump(feature_names, 'model/feature_names.pkl')
joblib.dump(label_encoders, 'model/label_encoders.pkl')
print(f"  ✓ Feature metadata saved")

print("\n" + "=" * 80)
print("✓ TRAINING COMPLETE - Model ready for prediction!")
print("=" * 80)
print(f"\nModel Location: model/churn_model.pkl")
print(f"Scaler Location: model/scaler.pkl")
print(f"\nStart the backend: python app.py")
print("=" * 80)
