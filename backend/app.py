import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# ============================================================================
# DATABASE SETUP
# ============================================================================
DATABASE_PATH = 'database/churnwise.db'

def get_db():
    """Get database connection"""
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with predictions table"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE,
            gender TEXT,
            senior_citizen INTEGER,
            partner TEXT,
            dependents TEXT,
            tenure INTEGER,
            phone_service TEXT,
            internet_service TEXT,
            online_security TEXT,
            online_backup TEXT,
            device_protection TEXT,
            tech_support TEXT,
            streaming_tv TEXT,
            streaming_movies TEXT,
            contract TEXT,
            paperless_billing TEXT,
            payment_method TEXT,
            monthly_charges REAL,
            total_charges REAL,
            probability REAL,
            prediction TEXT,
            risk_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# ============================================================================
# MODEL LOADING
# ============================================================================
model = None
scaler = None
feature_names = None
label_encoders = None

def load_model():
    """Load trained model and preprocessing artifacts"""
    global model, scaler, feature_names, label_encoders
    
    try:
        model = joblib.load('model/churn_model.pkl')
        scaler = joblib.load('model/scaler.pkl')
        feature_names = joblib.load('model/feature_names.pkl')
        label_encoders = joblib.load('model/label_encoders.pkl')
        print("✓ Model loaded successfully")
        return True
    except FileNotFoundError as e:
        print(f"✗ Model not found: {e}")
        print("Please train the model first: python model/train_model.py")
        return False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def preprocess_input(data):
    """Preprocess input data for prediction"""
    try:
        # Create feature array
        features = {}
        
        # Map input fields to feature names
        field_mapping = {
            'gender': 'gender',
            'senior_citizen': 'SeniorCitizen',
            'partner': 'Partner',
            'dependents': 'Dependents',
            'tenure': 'tenure',
            'phone_service': 'PhoneService',
            'internet_service': 'InternetService',
            'online_security': 'OnlineSecurity',
            'online_backup': 'OnlineBackup',
            'device_protection': 'DeviceProtection',
            'tech_support': 'TechSupport',
            'streaming_tv': 'StreamingTV',
            'streaming_movies': 'StreamingMovies',
            'contract': 'Contract',
            'paperless_billing': 'PaperlessBilling',
            'payment_method': 'PaymentMethod',
            'monthly_charges': 'MonthlyCharges',
            'total_charges': 'TotalCharges',
        }
        
        for input_key, feature_key in field_mapping.items():
            if input_key not in data:
                raise ValueError(f"Missing field: {input_key}")
            features[feature_key] = data[input_key]
        
        # Create DataFrame with feature names in correct order
        df = pd.DataFrame([features], columns=feature_names)
        
        # Encode categorical variables
        for col in df.columns:
            if col in label_encoders:
                try:
                    df[col] = label_encoders[col].transform(df[col].astype(str))
                except ValueError as e:
                    print(f"Warning: Could not encode {col}: {e}")
                    # Use first known class if value not seen during training
                    df[col] = label_encoders[col].transform([label_encoders[col].classes_[0]])[0]
        
        # Scale features
        df_scaled = scaler.transform(df)
        
        return df_scaled, True, None
    
    except Exception as e:
        return None, False, str(e)

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.40:
        return "LOW"
    elif probability < 0.70:
        return "MEDIUM"
    else:
        return "HIGH"

def get_important_factors(data):
    """Identify important factors contributing to churn risk"""
    factors = []
    
    # Month-to-month contract
    if data.get('contract') == 'Month-to-month':
        factors.append("Month-to-month contract increases churn risk")
    
    # Short tenure
    if data.get('tenure', 0) < 12:
        factors.append(f"Short tenure ({data.get('tenure')} months) indicates new customer")
    
    # High monthly charges
    if data.get('monthly_charges', 0) > 80:
        factors.append(f"High monthly charges (${data.get('monthly_charges'):.2f}) may cause dissatisfaction")
    
    # No tech support
    if data.get('tech_support') == 'No':
        factors.append("No technical support - consider offering support services")
    
    # No online security
    if data.get('online_security') == 'No':
        factors.append("No online security - security features reduce churn")
    
    # Fiber optic internet
    if data.get('internet_service') == 'Fiber optic':
        factors.append("Fiber optic service - quality issues may affect retention")
    
    # No backup service
    if data.get('online_backup') == 'No':
        factors.append("No online backup service")
    
    # Electronic check payment
    if data.get('payment_method') == 'Electronic check':
        factors.append("Electronic check payment method associated with higher churn")
    
    return factors[:5]  # Return top 5 factors

def get_recommendations(data, probability):
    """Generate retention recommendations"""
    recommendations = []
    
    # Based on contract
    if data.get('contract') == 'Month-to-month':
        recommendations.append("Offer upgrade to annual or 2-year contract with discount")
    
    # Based on tenure
    if data.get('tenure', 0) < 6:
        recommendations.append("Provide dedicated onboarding and customer success support")
    
    # Based on support services
    if data.get('tech_support') == 'No':
        recommendations.append("Offer free technical support trial period")
    
    if data.get('online_security') == 'No':
        recommendations.append("Bundle online security service at discounted rate")
    
    # Based on charges
    if data.get('monthly_charges', 0) > 100:
        recommendations.append("Offer loyalty discount or service optimization review")
    
    # High risk specific
    if probability > 0.75:
        recommendations.append("Schedule personal retention call from customer success team")
    
    return recommendations[:4]  # Return top 4 recommendations

def save_prediction(data, prediction, probability, risk_level):
    """Save prediction to database"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Generate customer ID if not provided
        customer_id = f"PRED_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cursor.execute('''
            INSERT INTO predictions (
                customer_id, gender, senior_citizen, partner, dependents,
                tenure, phone_service, internet_service, online_security,
                online_backup, device_protection, tech_support, streaming_tv,
                streaming_movies, contract, paperless_billing, payment_method,
                monthly_charges, total_charges, probability, prediction, risk_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_id,
            data.get('gender'),
            data.get('senior_citizen'),
            data.get('partner'),
            data.get('dependents'),
            data.get('tenure'),
            data.get('phone_service'),
            data.get('internet_service'),
            data.get('online_security'),
            data.get('online_backup'),
            data.get('device_protection'),
            data.get('tech_support'),
            data.get('streaming_tv'),
            data.get('streaming_movies'),
            data.get('contract'),
            data.get('paperless_billing'),
            data.get('payment_method'),
            data.get('monthly_charges'),
            data.get('total_charges'),
            probability,
            prediction,
            risk_level
        ))
        
        conn.commit()
        conn.close()
        return customer_id
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return None

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make churn prediction"""
    try:
        if not model:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Preprocess input
        X_scaled, success, error = preprocess_input(data)
        
        if not success:
            return jsonify({'error': f'Data preprocessing failed: {error}'}), 400
        
        # Make prediction
        prediction_proba = model.predict_proba(X_scaled)[0]
        churn_probability = float(prediction_proba[1])
        prediction = 'CHURN' if churn_probability > 0.5 else 'NO_CHURN'
        risk_level = get_risk_level(churn_probability)
        
        # Get factors and recommendations
        factors = get_important_factors(data)
        recommendations = get_recommendations(data, churn_probability)
        
        # Save to database
        customer_id = save_prediction(data, prediction, churn_probability, risk_level)
        
        return jsonify({
            'customer_id': customer_id,
            'prediction': prediction,
            'probability': round(churn_probability, 4),
            'risk_level': risk_level,
            'factors': factors,
            'recommendations': recommendations,
            'success': True
        }), 200
    
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute('SELECT COUNT(*) as count FROM predictions')
        total_predictions = cursor.fetchone()['count']
        
        # Churn predictions
        cursor.execute('SELECT COUNT(*) as count FROM predictions WHERE prediction = "CHURN"')
        churn_count = cursor.fetchone()['count']
        
        # Non-churn predictions
        non_churn_count = total_predictions - churn_count
        
        # Churn percentage
        churn_percentage = (churn_count / total_predictions * 100) if total_predictions > 0 else 0
        
        # Get recent predictions
        cursor.execute('''
            SELECT customer_id, probability, prediction, risk_level, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT 10
        ''')
        recent_predictions = [dict(row) for row in cursor.fetchall()]
        
        # Churn by contract
        cursor.execute('''
            SELECT contract, COUNT(*) as count, 
                   SUM(CASE WHEN prediction = "CHURN" THEN 1 ELSE 0 END) as churn_count
            FROM predictions
            GROUP BY contract
        ''')
        contract_data = [dict(row) for row in cursor.fetchall()]
        
        # Churn by internet service
        cursor.execute('''
            SELECT internet_service, COUNT(*) as count,
                   SUM(CASE WHEN prediction = "CHURN" THEN 1 ELSE 0 END) as churn_count
            FROM predictions
            GROUP BY internet_service
        ''')
        internet_data = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'total_predictions': total_predictions,
            'churn_count': churn_count,
            'non_churn_count': non_churn_count,
            'churn_percentage': round(churn_percentage, 2),
            'recent_predictions': recent_predictions,
            'by_contract': contract_data,
            'by_internet_service': internet_data,
            'success': True
        }), 200
    
    except Exception as e:
        print(f"Dashboard error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """Get prediction history"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        offset = (page - 1) * limit
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) as count FROM predictions')
        total = cursor.fetchone()['count']
        
        # Get paginated results
        cursor.execute('''
            SELECT * FROM predictions
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        predictions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'predictions': predictions,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit,
            'success': True
        }), 200
    
    except Exception as e:
        print(f"History error: {e}")
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'database': 'ready'
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'app': 'ChurnWise - AI Customer Churn Prediction System',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'predict': 'POST /api/predict',
            'dashboard': 'GET /api/dashboard',
            'history': 'GET /api/history',
            'health': 'GET /api/health'
        }
    }), 200

# ============================================================================
# STARTUP
# ============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("CHURNWISE - FLASK BACKEND SERVER")
    print("=" * 80)
    
    # Initialize database
    print("\n[1/3] Initializing database...")
    init_db()
    print("✓ Database ready")
    
    # Load model
    print("\n[2/3] Loading machine learning model...")
    if not load_model():
        print("✗ Model loading failed!")
        print("Please train the model first:")
        print("  cd backend")
        print("  python model/train_model.py")
        exit(1)
    
    print("\n[3/3] Starting Flask server...")
    print("\n" + "=" * 80)
    print("✓ Server running on http://localhost:5000")
    print("✓ API endpoints ready")
    print("=" * 80)
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='localhost', port=5000, use_reloader=False)
